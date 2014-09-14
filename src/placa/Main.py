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
from src.ws.ResultadoLecturaWS import ResultadoLecturaWS
from src.lecturas.Resultado import Resultado
from src.ws.ResultadoAccionWS import ResultadoAccionWS
from src.ws.ResultadoCreacionWS import ResultadoCreacionWS
import math
import time


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
    periodicidadLecturas= mbd.obtenerPeriodicidadLecturasPlaca(con)
    periodicidadNiveles= mbd.obtenerPeriodicidadNivelesPlaca(con)
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
    
    #aca la lista de grupos de actuadores ya está actualizada con la lista de actuadores de cada una 
    #Hay que cargar la lista de niveles de severidad
    listaNivelesSeveridad= mbd.obtenerListaNivelesSeveridad(con)
    for nivel in listaNivelesSeveridad:
        idFactor=nivel.get_factor()
        i=0
        while i<len(listaFactores) and listaFactores[i].get_id_factor() <> idFactor :
            i= i+1
        factor= listaFactores[i]
        nivel.set_factor(factor)
        perfil= nivel.get_perfil_activacion()
        idPerfil= perfil.get_id_perfil_activacion()
        listaIdGruposEstados= mbd.obtenerListaIdGruposActuadoresEstadosPerfil(con, idPerfil)
        listaGruposEstadosPerfil= list()
        for idGrupoEstado in listaIdGruposEstados:
            idGrupo= idGrupoEstado[0]
            j=0
            while idGrupo <> listaGrupoActuadores[j].get_id_grupo_actuador():
                j= j+1
            grupo= listaGrupoActuadores[j]
            estadoGrupo= idGrupoEstado[1]
            tupla= (grupo, estadoGrupo)
            listaGruposEstadosPerfil.append(tupla)
        perfil.set_lista_grupo_actuadores_estado(listaGruposEstadosPerfil)
        nivel.set_perfil_activacion(perfil)

    mbd.cerrarConexion()
    #Tengo todo lo necesario para instanciar el objeto Placa
    try:
        h= Herramientas()
        ik= h.instanciarIK(int(nroSerie))
        if ik <> None:
            placa= Placa(nroSerie, estadoSistema, periodicidadLecturas, periodicidadNiveles, listaDispositivos, listaGrupoActuadores, listaFactores, listaNivelesSeveridad) 
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
            server = make_server('192.168.1.44', 7789, Comunicacion())
            server.serve_forever()
        except ImportError:
            print ("Error: example server code requires Python >= 2.5")
            
class tomarLecturas(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    
    def run(self):
        placa= getPlaca()
        listaFactores= placa.get_lista_factores()
        while (placa.get_estado_sistema() == 'A' or placa.get_estado_sistema() == 'M'):
            for factor in listaFactores:
                procesarLecturaFactor(factor)
            time.sleep(placa.get_periodicidad_lecturas())
            
class procesarNiveles(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    
    def run(self):
        placa= getPlaca()
        listaNiveles= placa.get_lista_niveles_severidad()
        while (placa.get_estado_sistema() == 'A' or placa.get_estado_sistema() == 'M'):
            listaNivelesValidos= list()
            for nivel in listaNiveles:
                factor= nivel.get_factor()
                idFactor= factor.get_id_factor()
                mbd= ManejadorBD()
                con= mbd.getConexion()
                cantidadLecturas= placa.get_periodicidad_niveles() / placa.get_periodicidad_lecturas()
                listaValoresLecturas=mbd.obtenerLecturasFactorCantidad(con, idFactor, cantidadLecturas)
                cumpleNivel= analizarCumplimientoNivel(listaValoresLecturas, nivel.get_rango_minimo(), nivel.get_rango_maximo())
                if cumpleNivel:
                    listaNivelesValidos.append(nivel)
            #ordenar lista por prioridad
            listaNivelesValidos.sort()
            """Después sacar esta salida a consola"""
            for nivel in listaNivelesValidos:
                print("Nivel válido: "+nivel.get_nombre()+"; prioridad: "+str(nivel.get_prioridad()))
            """hasta acá"""
            listaActivacion= list()
            for nivel in listaNivelesValidos:
                perfil= nivel.get_perfil_activacion()
                listaGrupoActuadoresEstado= perfil.get_lista_grupo_actuadores_estado()
                for grupoEstado in listaGrupoActuadoresEstado:
                    i= 0
                    while i < len(listaActivacion) and listaActivacion[i][0].get_id_grupo_actuador() <> grupoEstado[0].get_id_grupo_actuador() :
                        i=i+1
                    if i >= len(listaActivacion):
                        listaActivacion.append(grupoEstado)
            """YA TENGO TODO LO NECESARIO PARA ACTUAR SOBRE LOS GRUPOS DE ACTUADORES SEGÚN SE HAYA ESPECIFICADO EN EL 
            PERFIL DE ACTIVACION DE CADA NIVEL DE SEVERIDAD QUE SE ESTÁ CUMPLIENDO"""
            for grupoEstado in listaActivacion:
                grupo= grupoEstado[0]
                estado= grupoEstado[1]
                if estado == 'E':
                    encenderGrupoActuadores(grupo)
                elif estado == 'A':
                    apagarGrupoActuadores(grupo)
                else:
                    print ("Estado no válido para perfil de activación")
                    
            time.sleep(placa.get_periodicidad_niveles())
            
def analizarCumplimientoNivel( listaValoresLecturas, minimo, maximo):
    cantidadLecturas= len(listaValoresLecturas)
    objetivoLecturas= int((Propiedades.porcentajeLecturasProcNiveles * cantidadLecturas) / 100)
    coincidencias= 0
    for lectura in listaValoresLecturas:
        if lectura >= minimo and lectura <= maximo:
            coincidencias= coincidencias +1 
    cumple= coincidencias >= objetivoLecturas
    return cumple    
                
        

def cambiarEstadoPlaca(estado):
    __placa.set_estado_sistema(estado)
    mbd= ManejadorBD()
    con= mbd.getConexion()
    mbd.cambiarEstadoPlaca(con, estado)
    con.commit()
    con.close()
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

def crearSensor (nombre, modelo, nroPuerto, formulaConversion, idTipoPuerto, idPlacaPadre, idFactor):
    mbd= ManejadorBD()
    con= mbd.getConexion()
    idDispositivo=mbd.insertarDispositivo(con, nombre, modelo, nroPuerto)
    con.commit()
    mbd.insertarSensor(con, idDispositivo, formulaConversion, idTipoPuerto, idPlacaPadre, idFactor)
    con.commit()
    return idDispositivo

def crearActuador (nombre, modelo, nroPuerto, idTipoPuerto, idTipoActuador, idPlacaPadre, idGrupoActuadores):
    mbd= ManejadorBD()
    con= mbd.getConexion()
    idDispositivo=mbd.insertarDispositivo(con, nombre, modelo, nroPuerto)
    con.commit()
    mbd.insertarActuador(con, idDispositivo, idTipoPuerto, idTipoActuador, idPlacaPadre, idGrupoActuadores)
    con.commit()
    return idDispositivo

def crearPlacaAuxiliar (nombre, modelo, nroPuerto, nroSerie, idTipoPlaca, idPlacaPadre):
    mbd= ManejadorBD()
    con= mbd.getConexion()
    idDispositivo=mbd.insertarDispositivo(con, nombre, modelo, nroPuerto)
    con.commit()
    mbd.insertarPlacaAuxiliar(con, idDispositivo, nroSerie, idTipoPlaca, idPlacaPadre)
    con.commit()
    return idDispositivo

def crearTipoPlaca (nombre):
    mbd= ManejadorBD()
    con= mbd.getConexion()
    idTipoPlaca=mbd.insertarTipoPlaca(con, nombre)
    con.commit()
    return idTipoPlaca

def crearTipoActuador (nombre):
    mbd= ManejadorBD()
    con= mbd.getConexion()
    idTipoActuador=mbd.insertarTipoActuador(con, nombre)
    con.commit()
    return idTipoActuador

def eliminarDispositivo (dispositivo): #pendiente
    #tener en cuenta q si es una placa auxiliar hay que verificar q no tenga en su lista de dispositivos ninguno activo
    return None

def iniciarComportamientoAutomatico():
    
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
    fecha= datetime.now()
    idFactor= factor.get_id_factor()
    resultadoLectura= ResultadoLectura(mensaje, fecha, idFactor, lecturaFinal)
    mbd.insertarLecturaFactor(con, idFactor, fecha, lecturaFinal)
    con.commit()
    con.close()
    return resultadoLectura

def crearFactor(nombre, unidad, valorMin, valorMax):
    mbd= ManejadorBD()
    con= mbd.getConexion()
    idFactor=mbd.insertarFactor(con, nombre, unidad, valorMin, valorMax)
    con.commit()
    con.close()
    return idFactor

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

def crearGrupoActuadores(nombre):
    mbd= ManejadorBD()
    con= mbd.getConexion()
    idGrupo=mbd.insertarGrupoActuadores(con, nombre)
    con.commit()
    con.close()
    return idGrupo


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

def convertirResultadoLectura(resultadoLectura):
    mensaje= resultadoLectura.get_mensaje()
    fecha= resultadoLectura.get_fecha()
    idFactor= resultadoLectura.get_id_factor()
    valor= resultadoLectura.get_valor()
    resultado= ResultadoLecturaWS(mensaje, fecha, idFactor, valor)
    return resultado

def convertirResultadoAccion(resultadoAccion):
    mensaje= resultadoAccion.get_mensaje()
    fecha= resultadoAccion.get_fecha()
    idGrupoActuadores= resultadoAccion.get_id_grupo_actuadores()
    tipoAccion= resultadoAccion.get_tipo_accion()
    resultado= ResultadoAccionWS(mensaje, fecha, idGrupoActuadores, tipoAccion)
    return resultado

class Comunicacion(SimpleWSGISoapApp):
    
    @soapmethod(Integer,_returns=ResultadoAccionWS)
    def wsEncenderGrupoActuadores(self, idGrupo):
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
            resultadoWS= convertirResultadoAccion(resultado)
        else:
            idMensaje= Mensajes.noExisteGrupoActuadores
            mbd= ManejadorBD()
            con= mbd.getConexion()
            mensaje=mbd.obtenerMensaje(con, idMensaje)
            con.close()
            fecha= datetime.now()
            tipoAccion= ""
            resultadoWS= ResultadoAccionWS(mensaje, fecha, idGrupo, tipoAccion)
        return resultadoWS
    
    @soapmethod(Integer,_returns=ResultadoAccionWS)
    def wsApagarGrupoActuadores(self, idGrupo):
        placa= getPlaca()
        listaGrupoActuadores= placa.get_lista_grupo_actuadores()
        mensaje= None
        grupo=None
    
        i=0
        while i < len(listaGrupoActuadores) and idGrupo <> listaGrupoActuadores[i].get_id_grupo_actuador():
            i= i+1
        if i < len(listaGrupoActuadores):
            grupo= listaGrupoActuadores[i]
            resultado=apagarGrupoActuadores(grupo)
            resultadoWS= convertirResultadoAccion(resultado)
        else:
            idMensaje= Mensajes.noExisteGrupoActuadores
            mbd= ManejadorBD()
            con= mbd.getConexion()
            mensaje=mbd.obtenerMensaje(con, idMensaje)
            con.close()
            fecha= datetime.now()
            tipoAccion= ""
            resultadoWS= ResultadoAccionWS(mensaje, fecha, idGrupo, tipoAccion)
        return resultadoWS
    
    @soapmethod(Integer,_returns=ResultadoLecturaWS)
    def wsLecturaFactor(self, idFactor):
        placa= getPlaca()
        listaFactores= placa.get_lista_factores()
        mensaje= None
        factor=None
        i=0
        while i < len(listaFactores) and idFactor <> listaFactores[i].get_id_factor():
            i= i+1
        if i < len(listaFactores):
            factor= listaFactores[i]
            resultado=procesarLecturaFactor(factor)
            resultadoWS= convertirResultadoLectura(resultado)
        else:
            idMensaje= Mensajes.noExisteFactor
            mbd= ManejadorBD()
            con= mbd.getConexion()
            mensaje=mbd.obtenerMensaje(con, idMensaje)
            con.close()
            fecha= datetime.now()
            valor= 0
            resultadoWS=ResultadoLecturaWS(mensaje, fecha, idFactor, valor)
        return resultadoWS
    
    @soapmethod(String,_returns=Mensaje)
    def wsCambiarEstadoSistema(self, estado):
        cambiarEstadoPlaca(estado)
        idMensaje= Mensajes.cambioEstadoSistemaOk
        mbd= ManejadorBD()
        con= mbd.getConexion()
        mensaje=mbd.obtenerMensaje(con, idMensaje)
        con.close()
        return mensaje
    
    @soapmethod(String, String, Integer, Integer, _returns=ResultadoCreacionWS)
    def wsCrearFactor(self, nombre, unidad, valorMin, valorMax):
        idFactor= crearFactor(nombre, unidad, valorMin, valorMax)
        idMensaje= Mensajes.factorCreadoOk
        mbd= ManejadorBD()
        con= mbd.getConexion()
        mensaje=mbd.obtenerMensaje(con, idMensaje)
        con.close()
        resultado= ResultadoCreacionWS(mensaje, idFactor)
        return resultado
    
    @soapmethod(String, _returns=ResultadoCreacionWS)
    def wsCrearGrupoActuadores(self, nombre):
        idGrupo= crearGrupoActuadores(nombre)
        idMensaje= Mensajes.grupoActuadoresCreadoOk
        mbd= ManejadorBD()
        con= mbd.getConexion()
        mensaje=mbd.obtenerMensaje(con, idMensaje)
        con.close()
        resultado= ResultadoCreacionWS(mensaje, idGrupo)
        return resultado
    
    @soapmethod(String, _returns=ResultadoCreacionWS)
    def wsCrearSensor(self, nombre, modelo, nroPuerto, formulaConversion, idTipoPuerto, idPlacaPadre, idFactor):
        idSensor= crearSensor(nombre, modelo, nroPuerto, formulaConversion, idTipoPuerto, idPlacaPadre, idFactor)
        idMensaje= Mensajes.sensorCreadoOk
        mbd= ManejadorBD()
        con= mbd.getConexion()
        mensaje=mbd.obtenerMensaje(con, idMensaje)
        con.close()
        resultado= ResultadoCreacionWS(mensaje, idSensor)
        return resultado
    
    @soapmethod(String,String, Integer, Integer, Integer, Integer, Integer, _returns=ResultadoCreacionWS)
    def wsCrearActuador(self, nombre, modelo, nroPuerto, idTipoPuerto, idTipoActuador, idPlacaPadre, idGrupoActuadores):
        idActuador= crearActuador(nombre, modelo, nroPuerto, idTipoPuerto, idTipoActuador, idPlacaPadre, idGrupoActuadores)
        idMensaje= Mensajes.actuadorCreadoOk
        mbd= ManejadorBD()
        con= mbd.getConexion()
        mensaje=mbd.obtenerMensaje(con, idMensaje)
        con.close()
        resultado= ResultadoCreacionWS(mensaje, idActuador)
        return resultado
    
    @soapmethod(String, _returns=ResultadoCreacionWS)
    def wsCrearTipoPlaca(self, nombre):
        idTipoPlaca= crearTipoPlaca(nombre)
        idMensaje= Mensajes.tipoPlacaCreadaOk
        mbd= ManejadorBD()
        con= mbd.getConexion()
        mensaje=mbd.obtenerMensaje(con, idMensaje)
        con.close()
        resultado= ResultadoCreacionWS(mensaje, idTipoPlaca)
        return resultado
    
    @soapmethod(String, _returns=ResultadoCreacionWS)
    def wsCrearTipoActuador(self, nombre):
        idTipoActuador= crearTipoActuador(nombre)
        idMensaje= Mensajes.tipoActuadorCreadoOk
        mbd= ManejadorBD()
        con= mbd.getConexion()
        mensaje=mbd.obtenerMensaje(con, idMensaje)
        con.close()
        resultado= ResultadoCreacionWS(mensaje, idTipoActuador)
        return resultado
    
    @soapmethod(String,String, Integer, String, Integer, Integer, _returns=ResultadoCreacionWS)
    def wsCrearPlacaAuxiliar(self, nombre, modelo, nroPuerto, nroSerie, idTipoPlaca, idPlacaPadre):
        idPlacaAuxiliar= crearPlacaAuxiliar(nombre, modelo, nroPuerto, nroSerie, idTipoPlaca, idPlacaPadre)
        idMensaje= Mensajes.placaAuxiliarCreadaOk
        mbd= ManejadorBD()
        con= mbd.getConexion()
        mensaje=mbd.obtenerMensaje(con, idMensaje)
        con.close()
        resultado= ResultadoCreacionWS(mensaje, idPlacaAuxiliar)
        return resultado
    
    
        
    

if __name__ == '__main__':
    __placa=iniciarPlaca()
    t = iniciarWS()
    t.start()
    t2= tomarLecturas()
    t2.start()
    time.sleep(__placa.get_periodicidad_niveles())
    t3= procesarNiveles()
    t3.start()
    
    threading.activeCount()
    """
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
            
    listaNiveles= __placa.get_lista_niveles_severidad()
    for nivel in listaNiveles:
        print("Nivel: "+nivel.get_nombre())
        print("Factor: "+nivel.get_factor().get_nombre())
        print("Prioridad: "+str(nivel.get_prioridad()))
        print ("Rango Minimo: "+ str(nivel.get_rango_minimo()))
        print ("Rango Maximo: "+ str(nivel.get_rango_maximo()))
        perfil= nivel.get_perfil_activacion()
        listaGrupoEstado= perfil.get_lista_grupo_actuadores_estado()
        print("Perfil de activacion:")
        for grupoEstado in listaGrupoEstado:
            grupo= grupoEstado[0]
            estado= grupoEstado[1]
            print("Grupo: "+grupo.get_nombre() +", Estado: "+ estado)
    """
  
            
    
            
            
    
    
    