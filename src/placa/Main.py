# -*- encoding: utf-8 -*-
"""
Módulo principal del sistema, es el encargado de iniciar la ejecución del mismo.
Debe instanciar la placa y el servidor de WS, además es encargado de comunicarse con la 
capa de persistencia para guardar y recuperar datos.
Tiene como atributos una instancia única de placa y una instancia única de ws.
"""
from src.bdd.ManejadorBD import ManejadorBD
from src.placa.Placa import Placa
from Phidgets.PhidgetException import PhidgetException
from Phidgets.Devices.InterfaceKit import InterfaceKit
from src.recursos.Herramientas import Herramientas
from src.placa.PlacaAuxiliar import PlacaAuxiliar
from src.recursos import Propiedades, Mensajes
from src.lecturas.ResultadoLectura import ResultadoLectura
from datetime import datetime
from src.lecturas.ResultadoAccion import ResultadoAccion
import soaplib.core
from src.logs.Mensaje import Mensaje
from src.bdd.ManejadorBD import ManejadorBD
from src.recursos import Mensajes
from soaplib.wsgi_soap import SimpleWSGISoapApp
from soaplib.service import soapmethod
from soaplib.serializers.primitive import String, Integer, Array

import threading


__placa=None
__ws=None

def iniciarPlaca():
    """
    Método que inicializa la placa controladora y carga sus estructuras desde la BD
    """
    mbd= ManejadorBD()
    con= mbd.getConexion()
    estadoSistema= mbd.obtenerEstadoPlaca(con)
    nroSerie= mbd.obtenerNroSeriePlaca(con)
    listaDispositivos= mbd.obtenerListaDispositivos(con)
    listaFactores= mbd.obtenerListaFactores(con)
    for factor in listaFactores:
        idFactor= factor.get_id_factor()
        listaSensores= list()
        listaIdSensores=mbd.obtenerListaIdSensoresFactor(con, idFactor)
        for idSensor in listaIdSensores:
            i=0
            while i < len(listaDispositivos) and idSensor <>listaDispositivos[i].get_id_dispositivo():
                i= i+1
            if i < len(listaDispositivos):
                sensor= listaDispositivos[i]
                listaSensores.append(sensor)
        factor.set_lista_sensores(listaSensores)
    #aca la lista de factores ya está actualizada con la lista de sensores de cada una
    listaGrupoActuadores= mbd.obtenerListaGrupoActuadores(con)
    for grupo in listaGrupoActuadores:
        idGrupoActuadores= grupo.get_id_grupo_actuador()
        listaActuadores= list()
        listaIdActuadores=mbd.obtenerListaIdActuadoresGrupo(con, idGrupoActuadores)
        for idActuador in listaIdActuadores:
            actuador= obtenerDispositivoSegunId(listaDispositivos, idActuador)
            
            if actuador <> None:
                listaActuadores.append(actuador)
        grupo.set_lista_actuadores(listaActuadores)
    mbd.cerrarConexion()
    #aca la lista de grupos de actuadores ya está actualizada con la lista de actuadores de cada una 
    #Tengo todo lo necesario para instanciar el objeto Placa
    try:
        h= Herramientas()
        ik= h.instanciarIK(int(nroSerie))
        if ik <> None:
            placa= Placa(nroSerie, estadoSistema, listaDispositivos, listaGrupoActuadores, listaFactores) 
            placa.set_ik(ik)
        else:
            print('ERROR FATAL')
            #EMITIR ALERTA Y GENERAR LOG DE EVENTO
    except PhidgetException as e:
        print('No se pudo instanciar el ik de la placa controladora')
        #emitir alerta y generar log de evento    
    return placa

def obtenerDispositivoSegunId(listaDispositivos, idDispositivo):
    actuador=None
    i=0
    control= False
    while i < len(listaDispositivos) and (idDispositivo <>listaDispositivos[i].get_id_dispositivo()) and control == False:
        if isinstance(listaDispositivos[i], (PlacaAuxiliar)):
            actuador=obtenerDispositivoSegunId(listaDispositivos[i].get_lista_dispositivos(), idDispositivo)
        if actuador <> None:
            control= True
        i= i+1
    if i < len(listaDispositivos) and control == False:
        actuador= listaDispositivos[i]
    return actuador


class iniciarWS(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    
    def run(self):
        try:
            from wsgiref.simple_server import make_server
            server = make_server('localhost', 7789, Comunicacion())
            server.serve_forever()
        except ImportError:
            print ("Error: example server code requires Python >= 2.5")

def cambiarEstadoPlaca(estado):
    return None

def chequeoPlaca(): #DESPUES
    return None

def chequeoDispositivo(idDispositivo): #DESPUES
    return None

def chequeoDispositivos(): #DESPUES
    return None

def obtenerIkPadre (dispositivo):
    """Devuelve el interface kit que controla al dispositivo pasado como parámetro"""
    padre= dispositivo.get_padre()
    if padre == None:
        return __placa.get_ik()
    else:
        return padre.get_ik()
    

def lecturaSensor(sensor):
    """Método que permite obtener una lectura de un sensor conectado a un puerto analógico o digital,
    recibe como parámetros el sensor del que se pretende obtener la lectura y el interface kit que puede 
    interactuar con dicho sensor. Devuelve la lectura convertida a su valor final luego de aplicar la fórmula 
    propia del sensor"""
    ik= obtenerIkPadre (sensor)
    tipoPuerto= sensor.get_tipo_puerto()
    if tipoPuerto.get_nombre() == "analogico":
        try: 
            valor=ik.getSensorValue(sensor.get_numero_puerto())
            l=valor
            temp= eval(sensor.get_formula_conversion())
        except PhidgetException as e:
            temp= -1
    elif tipoPuerto.get_nombre() == "e-digital":
        try: 
            temp= ik.getInputState(sensor.get_numero_puerto())
        except PhidgetException as e:
            temp= -1
    return temp

def encenderActuador(actuador):
    """
    Método para encender un actuador perteneciente a un grupo de actuadores
    """
    estado= actuador.get_estado_actuador()
    if ( estado == 'A'):
        try:
            ik= obtenerIkPadre(actuador)
            if ik <> None:
                ik.setOutputState(actuador.get_numero_puerto(), 1) 
                estado= 'E'
                actuador.set_estado_actuador(estado)
                mbd= ManejadorBD()
                con= mbd.getConexion()
                mbd.cambiarEstadoActuador(con, actuador)
                con.commit()
                con.close()
            else:
                estado= 'F'
        except PhidgetException as e:
            estado= 'F'
    return estado

def apagarActuador(actuador):
    """
    Método para apagar un actuador perteneciente a un grupo de actuadores
    """
    estado= actuador.get_estado_actuador()
    if (estado == 'E'):
        try:
            ik= obtenerIkPadre (actuador)
            if ik <> None:
                ik.setOutputState(actuador.get_numero_puerto(), 0) 
                estado= 'A'
                actuador.set_estado_actuador(estado)   
                mbd= ManejadorBD()
                con= mbd.getConexion()
                mbd.cambiarEstadoActuador(con, actuador)
                con.commit()
                con.close()
            else:
                estado='F'
        except PhidgetException as e:
            estado= 'F'
    return estado

def encenderGrupoActuadores(grupo):
    """
    Método para encender un grupo de actuadores
    """
    listaAcciones= list()
    listaActuadores= grupo.get_lista_actuadores()
    for actuador in listaActuadores:
        if actuador.get_estado_actuador() == 'A':
            estadoActuador=encenderActuador(actuador)
            if estadoActuador == 'F':
                print('ERROR ENCENDIDO ACTUADOR')
                #EMITIR ALERTA Y GENERAR LOG DE EVENTO
            else:
                mbd= ManejadorBD()
                con= mbd.getConexion()
                idActuador= actuador.get_id_dispositivo()
                mbd.insertarAccionActuador(con, idActuador, estadoActuador)
                con.commit()
                con.close()
            listaAcciones.append(estadoActuador)
    if len(listaAcciones) == 0:
        #todos los actuadores estaban prendidos
        idMensaje=Mensajes.actuadoresPrendidos
        if grupo.get_estado() == 'A':
            grupo.set_estado('E')
            mbd= ManejadorBD()
            con= mbd.getConexion()
            mbd.cambiarEstadoGrupoActuadores(con, grupo)
            con.commit()
            con.close()
    else:
        error= True
        i=0
        while i<len(listaAcciones) and error:
            error= listaAcciones[i] == 'F'
            i= i+1
        if error == True:
            #falló el encendido de todos los dispositivos
            idMensaje= Mensajes.encendidoGrupoError
        else:
            exito= True
            i=0
            while i<len(listaAcciones) and exito:
                exito= listaAcciones[i] == 'E'
                i= i+1
            if exito == True:
                #se encendieron todos los dispositivos del grupo de actuadores
                idMensaje= Mensajes.encendidoGrupoOk
                grupo.set_estado('E')
                mbd= ManejadorBD()
                con= mbd.getConexion()
                mbd.cambiarEstadoGrupoActuadores(con, grupo)
                con.commit()
                con.close()
            else:
                #el grupo de actuadores se encendió parcialmente
                idMensaje=Mensajes.encendidoGrupoParcial
                grupo.set_estado('E')
                mbd= ManejadorBD()
                con= mbd.getConexion()
                mbd.cambiarEstadoGrupoActuadores(con, grupo)
                con.commit()
                con.close()
    mbd= ManejadorBD()
    con= mbd.getConexion()
    mensaje=mbd.obtenerMensaje(con, idMensaje)
    con.close()
    fecha= datetime.now()
    resultadoAccion= ResultadoAccion(mensaje, fecha, grupo.get_id_grupo_actuador(), grupo.get_estado())
    return resultadoAccion

def apagarGrupoActuadores(grupo):
    """
    Método para apagar un grupo de actuadores
    """
    listaAcciones= list()
    listaActuadores= grupo.get_lista_actuadores()
    for actuador in listaActuadores:
        if actuador.get_estado_actuador() == 'E':
            estadoActuador=apagarActuador(actuador)
            if estadoActuador == 'F':
                print('ERROR APAGADO ACTUADOR')
                #EMITIR ALERTA Y GENERAR LOG DE EVENTO
            else:
                mbd= ManejadorBD()
                con= mbd.getConexion()
                idActuador= actuador.get_id_dispositivo()
                mbd.insertarAccionActuador(con, idActuador, estadoActuador)
                con.commit()
                con.close()
            listaAcciones.append(estadoActuador)
    if len(listaAcciones) == 0:
        #todos los actuadores estaban APAGADOS
        idMensaje=Mensajes.actuadoresApagados
    else:
        error= True
        i=0
        while i<len(listaAcciones) and error:
            error= listaAcciones[i] == 'F'
            i= i+1
        if error == True:
            #falló el apagado de todos los dispositivos
            idMensaje= Mensajes.apagadoGrupoError
        else:
            exito= True
            i=0
            while i<len(listaAcciones) and exito:
                exito= listaAcciones[i] == 'A'
                i= i+1
            if exito == True:
                #se apagaron todos los dispositivos del grupo de actuadores
                idMensaje= Mensajes.apagadoGrupoOk
                grupo.set_estado('A')
                mbd= ManejadorBD()
                con= mbd.getConexion()
                mbd.cambiarEstadoGrupoActuadores(con, grupo)
                con.commit()
                con.close()
            else:
                #el grupo de actuadores se apagó parcialmente
                idMensaje=Mensajes.apagadoGrupoParcial
                grupo.set_estado('A')
                mbd= ManejadorBD()
                con= mbd.getConexion()
                mbd.cambiarEstadoGrupoActuadores(con, grupo)
                con.commit()
                con.close()
    mbd= ManejadorBD()
    con= mbd.getConexion()
    mensaje=mbd.obtenerMensaje(con, idMensaje)
    con.close()
    fecha= datetime.now()
    resultadoAccion= ResultadoAccion(mensaje, fecha, grupo.get_id_grupo_actuador(), grupo.get_estado())
    return resultadoAccion

def cargarNivelPerfil(nivelSeveridad, perfilActivacion): #DESPUES
    return None

def eliminarNivelPerfil (idNivelSeveridad): #DESPUES
    return None

def cargarDispositivo (dispositivo): #DESPUES
    return None

def eliminarDispositivo (dispositivo): #pendiente
    #tener en cuenta q si es una placa auxiliar hay que verificar q no tenga en su lista de dispositivos ninguno activo
    return None

def iniciarComportamientoAutomatico(): #DESPUES
    return None

def detenerComportamientoAutomatico(control): #DESPUES
    return None

def iniciarChequeosAutomaticos(): #DESPUES
    return None

def analizarLecturas(listaLecturas, factor):
    """
    Método para procesar una lista de lecturas de un factor pasado como parámetro.
    Realiza la selección de lecturas válidas y determina si alguna de estas está fuera de rango
    """
    lecturasOk= list()
    if len(listaLecturas) > 1:
        for lectura in listaLecturas:
            promedioResto= (sum(listaLecturas) - lectura) / (len(listaLecturas) - 1)
            diferencia= lectura - promedioResto
            if diferencia < 0:
                diferencia= diferencia * -1
            if diferencia < Propiedades.umbralTemperatura:
                lecturasOk.append(lectura)
            else:
                print 'LECTURA FUERA DE UMBRAL PERMITIDO'
                #GENERAR ALERTA Y LOG EVENTO
            if lectura < factor.get_valor_min() or lectura > factor.get_valor_max() :
                print 'LECTURA FUERA DE RANGO'
                #GENERAR ALERTA LOG DE EVENTOS
    else:
        lectura= listaLecturas[0]
        if lectura < factor.get_valor_min() or lectura > factor.get_valor_max() :
                print 'LECTURA FUERA DE RANGO'
                #GENERAR ALERTA LOG DE EVENTOS
        lecturasOk.append(lectura)
    resultado= sum(lecturasOk) / len(lecturasOk) 
    return resultado
        

def procesarLecturaFactor(factor): 
    """Método que posibilita tomar lecturas de todos los sensores pertenecientes a un factor y devuelve
    un promedio de dichas lecturas como una única lectura perteneciente al factor.
    Recibe como parámetros un factor y un interfaceKit que permite interactuar con cada sensor.
    Devuelve una lectura promedio en formato float"""
    listaSensores= factor.get_lista_sensores()
    listaLecturas= list()
    for sensor in listaSensores:
        lectura=lecturaSensor(sensor)
        if lectura < 0:
            print('ERROR DE LECTURA')
            #generar log de eventos
        else:
            mbd= ManejadorBD()
            con= mbd.getConexion()
            mbd.insertarLecturaSensor(con, sensor.get_id_dispositivo(), lectura)
            con.commit()
            con.close()
            listaLecturas.append(lectura)
    lecturaFinal= -1
    if len(listaLecturas) == 0:
        idMensaje= Mensajes.lecturaError
    else:
        lecturaFinal= analizarLecturas(listaLecturas, factor)
        if lecturaFinal < factor.get_valor_min() or lecturaFinal > factor.get_valor_max():
            idMensaje= Mensajes.lecturaFueraRango
        else:
            idMensaje= Mensajes.lecturaExitosa
    mbd= ManejadorBD()
    con= mbd.getConexion()
    mensaje=mbd.obtenerMensaje(con, idMensaje)
    con.close()
    fecha= datetime.now()
    resultadoLectura= ResultadoLectura(mensaje, fecha, factor.get_id_factor(), lecturaFinal)
    return resultadoLectura

def crearFactor(factor): #DESPUES
    return None

def eliminarFactor(factor):
    """
    Método para realizar el eliminado lógico de un factor del sistema
    """
    #falta controlar que para cada sensor perteneciente a la lista del factor este no este activo en el sistema
    mbd= ManejadorBD()
    con= mbd.getConexion()
    idFactor= factor.get_id_factor()
    mbd.eliminadoLogicoGrupoActuadores(con, idFactor)
    con.commit()
    con.close()
    factor.set_activo_sistema('N')
    return None

def crearGrupoActuadores(grupoActuadores): #DESPUES
    return None

def eliminarGrupoActuadores(grupoActuadores):
    """
    Método para realizar el eliminado lógico de un grupo de actuadores del sistema
    """
    #falta controlar que para cada actuador en su lista no este activo en el sistema
    mbd= ManejadorBD()
    con= mbd.getConexion()
    idGrupoActuadores= grupoActuadores.get_id_grupo_actuador()
    mbd.eliminadoLogicoGrupoActuadores(con, idGrupoActuadores)
    con.commit()
    con.close()
    grupoActuadores.set_activo_sistema('N')
    return None

def pruebaWS(idGrupo):
    print('Desde el ws intenta llamar al id: '+str(idGrupo))
    
def getPlaca():
    return __placa

class Comunicacion(SimpleWSGISoapApp):
    
    @soapmethod(Integer,_returns=Mensaje)
    def encenderGrupoActuadores(self, idGrupo):
        placa= getPlaca()
        listaGrupoActuadores= placa.get_lista_grupo_actuadores()
        mensaje= None
        grupo=None
        i=0
        while i < len(listaGrupoActuadores) and idGrupo <> listaGrupoActuadores[i].get_id_grupo_actuador():
            i= i+1
        if i < len(listaGrupoActuadores):
            grupo= listaGrupoActuadores[i]
            resultado=encenderGrupoActuadores(grupo)
            mensaje= resultado.get_mensaje()
            print('Obtiene el mensaje: '+mensaje.get_texto())
            #return mensaje
        else:
            print ('No existe grupo de actuadores')
            idMensaje= Mensajes.noExisteGrupoActuadores
            mbd= ManejadorBD()
            con= mbd.getConexion()
            mensaje=mbd.obtenerMensaje(con, idMensaje)
            con.close()
            #return mensaje
            #mensaje.get_texto()
        return mensaje
        
    

if __name__ == '__main__':
    __placa=iniciarPlaca()
    t = iniciarWS()
    t.start()
    threading.activeCount()

    h= Herramientas()
    listaFactores= __placa.get_lista_factores()
    for factor in listaFactores:
        resultado=procesarLecturaFactor(factor)
        print ('Factor: '+str(resultado.get_id_factor()) +'; '+factor.get_nombre())
        print (resultado.get_mensaje().get_texto())
        print ('Fecha: '+str(resultado.get_fecha()))
        print ('Valor: '+str(resultado.get_valor()) +' '+factor.get_unidad())
    listaGrupo= __placa.get_lista_grupo_actuadores()
    for grupo in listaGrupo:
        print('Estado actual del grupo: '+ grupo.get_estado() )
        if grupo.get_estado() == 'A':
            resultado=encenderGrupoActuadores(grupo)
            print('Grupo Actuadores: '+str(resultado.get_id_grupo_actuadores())+'; '+grupo.get_nombre())
            print(resultado.get_mensaje().get_texto())
            print ('Fecha: '+str(resultado.get_fecha()))
            print ('Estado: '+resultado.get_tipo_accion())
        else:
            resultado=apagarGrupoActuadores(grupo)
            print('Grupo Actuadores: '+str(resultado.get_id_grupo_actuadores())+'; '+grupo.get_nombre())
            print(resultado.get_mensaje().get_texto())
            print ('Fecha: '+str(resultado.get_fecha()))
            print ('Estado: '+resultado.get_tipo_accion())

  
            
    
            
            
    
    
    