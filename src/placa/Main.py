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
from src.recursos import Propiedades, Mensajes, TiposLogs
from src.lecturas.ResultadoLectura import ResultadoLectura
from datetime import datetime
from src.lecturas.ResultadoAccion import ResultadoAccion
import soaplib.core
from src.logs.Mensaje import Mensaje
from src.bdd.ManejadorBD import ManejadorBD
from src.recursos import Mensajes
from soaplib.wsgi_soap import SimpleWSGISoapApp
from soaplib.service import soapmethod
from soaplib.serializers.primitive import String, Integer
import threading
from src.ws.ResultadoLecturaWS import ResultadoLecturaWS
from src.lecturas.Resultado import Resultado
from src.ws.ResultadoAccionWS import ResultadoAccionWS
from src.ws.ResultadoCreacionWS import ResultadoCreacionWS
import math
import time
from src.placa.ActuadorAvance import ActuadorAvance
from src.logs.LogEvento import LogEvento
from src.logs.SMS import SMS

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
        deAvance= grupo.get_de_avance()
        listaActuadores= list()
        listaIdActuadores=mbd.obtenerListaIdActuadoresGrupo(con, idGrupoActuadores, deAvance)
        for idActuador in listaIdActuadores:
            actuador= obtenerDispositivoSegunId(listaDispositivos, idActuador)
            if actuador <> None:
                listaActuadores.append(actuador)
            if isinstance(actuador, (ActuadorAvance)):
                #Se carga la lista de posiciones de este actuador de avance
                listaPosiciones= actuador.get_lista_posiciones()
                for posicion in listaPosiciones:
                    idPosicion= posicion.get_posicion()
                    listaIdSensores= mbd.obtenerListaIdSensoresPosicion(con, actuador.get_id_dispositivo(), idPosicion)
                    listaSensores= list()
                    for idSensor in listaIdSensores:
                        sensor= obtenerDispositivoSegunId(listaDispositivos, idSensor)
                        listaSensores.append(sensor)
                    posicion.set_lista_sensores(listaSensores)
      
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
    h= Herramientas()
    ik= h.instanciarIK(int(nroSerie))
    placa= None
    if ik <> None:
        placa= Placa(nroSerie, estadoSistema, periodicidadLecturas, periodicidadNiveles, listaDispositivos, listaGrupoActuadores, listaFactores, listaNivelesSeveridad) 
        placa.set_ik(ik)
        chequearPlacasAuxiliares(listaDispositivos)
    else:
        print('ERROR FATAL')
        idTipoLog= TiposLogs.noSePuedeInstanciarPC
        idMensaje= Mensajes.noSePuedeInstanciarPlacaControladora            
        generarLogEvento(idTipoLog, idMensaje, 0)

    return placa

def chequearPlacasAuxiliares(listaDispositivos):
    for dispositivo in listaDispositivos:
        if isinstance(dispositivo, (PlacaAuxiliar)):
            if dispositivo.get_ik() == None:
                idTipoLog= TiposLogs.noSePuedeInstanciarPlacaAuxiliar
                idMensaje= Mensajes.noSePuedeInstanciarPlacaAuxiliar
                generarLogEvento(idTipoLog, idMensaje, dispositivo)
            chequearPlacasAuxiliares(dispositivo.get_lista_dispositivos())
    

def obtenerDispositivoSegunId(listaDispositivos, idDispositivo):
    dispositivo=None
    i=0
    control= False
    while i < len(listaDispositivos) and (idDispositivo <> listaDispositivos[i].get_id_dispositivo()) and control == False:
        if isinstance(listaDispositivos[i], (PlacaAuxiliar)):
            dispositivo=obtenerDispositivoSegunId(listaDispositivos[i].get_lista_dispositivos(), idDispositivo)
        if dispositivo <> None:
            control= True
        i= i+1
    if i < len(listaDispositivos) and control == False:
        dispositivo= listaDispositivos[i]
    return dispositivo

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
        while (placa.get_estado_sistema() == 'A'):
            time.sleep(placa.get_periodicidad_niveles())
            if (placa.get_estado_sistema() == 'A'):
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
                    if grupo.get_de_avance() == 'S':
                        cambiarPosicionGrupoActuadores(grupo, int(estado))
                    else:
                        if estado == 'E':
                            encenderGrupoActuadores(grupo)
                        elif estado == 'A':
                            apagarGrupoActuadores(grupo)
                        else:
                            print ("Estado no válido para perfil de activación")
            
            
def analizarCumplimientoNivel( listaValoresLecturas, minimo, maximo):
    cantidadLecturas= len(listaValoresLecturas)
    objetivoLecturas= int((Propiedades.porcentajeLecturasProcNiveles * cantidadLecturas) / 100)
    coincidencias= 0
    for lectura in listaValoresLecturas:
        if lectura >= minimo and lectura < maximo:
            coincidencias= coincidencias +1 
    cumple= coincidencias >= objetivoLecturas
    return cumple  

def apagarTodo():
    listaGruposActuadores= __placa.get_lista_grupo_actuadores()
    for grupoActuadores in listaGruposActuadores:
        if grupoActuadores.get_de_avance() == 'N':
            apagarGrupoActuadores(grupoActuadores)

def cambiarEstadoPlaca(estado):
    placa= getPlaca()
    estadoActual= placa.get_estado_sistema()
    placa.set_estado_sistema(estado)
    mbd= ManejadorBD()
    con= mbd.getConexion()
    mbd.cambiarEstadoPlaca(con, estado)
    con.commit()
    con.close()
    if estado == 'I':
        """Si paso a estado inactivo desde cualquier otro estado debo apagar todos los dispositivos"""
        apagarTodo()
    elif estado == 'M':
        if estadoActual == 'I' or estadoActual == 'C':
            __placa=iniciarPlaca()
            iniciarHiloLecturas()
    elif estado == 'A':
        if estadoActual == 'I' or estadoActual == 'C':
            __placa=iniciarPlaca()
            iniciarHiloLecturas()
        iniciarHiloNiveles()
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
            if valor == 0:
                temp=-999
            else:
                l=valor
                temp= eval(sensor.get_formula_conversion())
        except PhidgetException as e:
            temp= -999
    elif tipoPuerto.get_nombre() == "e-digital":
        try: 
            temp= ik.getInputState(sensor.get_numero_puerto())
        except PhidgetException as e:
            temp= -999
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
                idTipoLog= TiposLogs.errorEncendidoActuador
                idMensaje= Mensajes.encendidoActuadorError   
                generarLogEvento(idTipoLog, idMensaje, actuador)
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
                idTipoLog= TiposLogs.errorApagadoActuador
                idMensaje= Mensajes.apagadoActuadorError  
                generarLogEvento(idTipoLog, idMensaje, actuador)
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

def crearActuadorAvance (nombre, modelo, nroPuerto, posicion, idTipoPuerto, idTipoActuador, idPlacaPadre, nroPuertoRetroceso, tipoPuertoRetroceso, tiempoEntrePosiciones, idGrupoActuadores):
    mbd= ManejadorBD()
    con= mbd.getConexion()
    idDispositivo=mbd.insertarDispositivo(con, nombre, modelo, nroPuerto)
    con.commit()
    mbd.insertarActuadorAvance(con, idDispositivo, posicion, idTipoPuerto, idTipoActuador, idPlacaPadre, nroPuertoRetroceso, tipoPuertoRetroceso, tiempoEntrePosiciones, idGrupoActuadores)
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

def crearNivelSeveridad (nombre, idFactor, prioridad, rangoMinimo, rangoMaximo):
    mbd= ManejadorBD()
    con= mbd.getConexion()
    idNivel=mbd.insertarNivelSeveridad(con, nombre, idFactor, prioridad, rangoMinimo, rangoMaximo)
    con.commit()
    con.close()
    return idNivel

def agregarFilaPerfilActivacion (idPerfilActivacion, idGrupoActuadores, estado):
    mbd= ManejadorBD()
    con= mbd.getConexion()
    mbd.insertarFilaPerfilActivacion(con, idPerfilActivacion, idGrupoActuadores, estado)
    con.commit()
    con.close()
    return None

def agregarPosicionActuadorAvance (idActuadorAvance, numeroPosicion, descripcion, valor):
    mbd= ManejadorBD()
    con= mbd.getConexion()
    mbd.insertarPosicionActuadorAvance(con, idActuadorAvance, numeroPosicion, descripcion, valor)
    con.commit()
    con.close()
    return None

def agregarSensorPosicionActuadorAvance (idSensor, idActuadorAvance, numeroPosicion):
    mbd= ManejadorBD()
    con= mbd.getConexion()
    mbd.insertarSensorPosicionActuadorAvance(con, idSensor, idActuadorAvance, numeroPosicion)
    con.commit()
    con.close()
    return None

def analizarLecturas(listaLecturas, factor):
    """
    Método para procesar una lista de lecturas de un factor pasado como parámetro.
    Realiza la selección de lecturas válidas y determina si alguna de estas está fuera de rango
    """
    lecturasOk= list()
    listaValores= list()
    for tupla in listaLecturas:
        listaValores.append(tupla[0])
    if len(listaLecturas) > 1:
        for tuplaLectura in listaLecturas:
            lectura= tuplaLectura[0]
            promedioResto= (sum(listaValores) - lectura) / (len(listaValores) - 1)
            diferencia= lectura - promedioResto
            if diferencia < 0:
                diferencia= diferencia * -1
            if diferencia < factor.get_umbral():
                lecturasOk.append(lectura)
            else:
                print 'LECTURA FUERA DE UMBRAL PERMITIDO'
                idTipoLog= TiposLogs.lecturaFueraUmbral
                idMensaje= Mensajes.lecturaFueraUmbral
                sensor= tuplaLectura[1]
                generarLogEvento(idTipoLog, idMensaje, sensor)
            if lectura < factor.get_valor_min() or lectura > factor.get_valor_max() :
                print 'LECTURA FUERA DE RANGO'
                idTipoLog= TiposLogs.lecturaFueraRango
                idMensaje= Mensajes.lecturaFueraRango
                sensor= tuplaLectura[1]
                generarLogEvento(idTipoLog, idMensaje, sensor)
    else:
        lectura= listaLecturas[0][0]
        if lectura < factor.get_valor_min() or lectura > factor.get_valor_max() :
            print 'LECTURA FUERA DE RANGO'
            #GENERAR ALERTA LOG DE EVENTOS
            idTipoLog= TiposLogs.lecturaFueraRango
            idMensaje= Mensajes.lecturaFueraRango
            sensor= listaLecturas[0][1]
            generarLogEvento(idTipoLog, idMensaje, sensor)
        lecturasOk.append(lectura)
    if len(lecturasOk) == 0:
        print ('NINGUNA LECTURA VÁLIDA')
        return 'E'
    else: 
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
        lectura=(lecturaSensor(sensor), sensor)
        mbd= ManejadorBD()
        con= mbd.getConexion()
        mbd.insertarLecturaSensor(con, sensor.get_id_dispositivo(), lectura[0])
        con.commit()
        con.close()
        if lectura[0] == -999:
            idTipoLog= TiposLogs.errorLecturaSensor
            idMensaje= Mensajes.lecturaError
            generarLogEvento(idTipoLog, idMensaje, sensor)
        else:
            listaLecturas.append(lectura)
    lecturaFinal= -999
    if len(listaLecturas) == 0:
        idMensaje= Mensajes.lecturaError
    else:
        lecturaFinal= analizarLecturas(listaLecturas, factor)
        if lecturaFinal == 'E':
            lecturaFinal = -999
            idMensaje = idMensaje= Mensajes.lecturaError
        else:
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

def crearFactor(nombre, unidad, valorMin, valorMax, umbral):
    mbd= ManejadorBD()
    con= mbd.getConexion()
    idFactor=mbd.insertarFactor(con, nombre, unidad, valorMin, valorMax, umbral)
    con.commit()
    con.close()
    return idFactor

def crearGrupoActuadores(nombre, deAvance):
    mbd= ManejadorBD()
    con= mbd.getConexion()
    idGrupo=mbd.insertarGrupoActuadores(con, nombre, deAvance)
    con.commit()
    con.close()
    return idGrupo

def eliminarFactor(idFactor):
    """
    Método para realizar el eliminado lógico de un factor del sistema
    """
    mbd= ManejadorBD()
    con= mbd.getConexion()
    mbd.eliminadoLogicoFactor(con, idFactor)
    con.commit()
    con.close()
    return None

def eliminarDispositivo(idDispositivo):
    """
    Método para realizar el eliminado lógico de un dispositivo del sistema
    """
    mbd= ManejadorBD()
    con= mbd.getConexion()
    mbd.eliminadoLogicoDispositivo(con, idDispositivo)
    con.commit()
    con.close()
    return None

def eliminarGrupoActuadores(idGrupoActuadores):
    """
    Método para realizar el eliminado lógico de un grupo de actuadores del sistema
    """
    mbd= ManejadorBD()
    con= mbd.getConexion()
    mbd.eliminadoLogicoGrupoActuadores(con, idGrupoActuadores)
    con.commit()
    con.close()
    return None

def eliminarNivelSeveridad(idNivelSeveridad):
    """
    Método para realizar el eliminado lógico de un grupo de actuadores del sistema
    """
    mbd= ManejadorBD()
    con= mbd.getConexion()
    mbd.eliminadoLogicoNivelSeveridad(con, idNivelSeveridad)
    con.commit()
    con.close()
    return None

def eliminarFilaPerfilActivacion(idPerfil, idGrupoActuadores):
    """
    Método para realizar el eliminado lógico de un grupo de actuadores del sistema
    """
    mbd= ManejadorBD()
    con= mbd.getConexion()
    mbd.eliminadoLogicoFilaPerfilActivacion(con, idPerfil, idGrupoActuadores)
    con.commit()
    con.close()
    return None

def generarLogEvento(idTipoLog, idMensaje, dispositivo):
    mbd= ManejadorBD()
    con= mbd.getConexion()
    tipoLogEvento=mbd.obtenerTipoLogEvento(con, idTipoLog)
    mensaje=mbd.obtenerMensaje(con, idMensaje)
    fecha= datetime.now()
    if dispositivo <> 0:
        idLogEvento=mbd.insertarLogEvento(con, idTipoLog, dispositivo.get_id_dispositivo(), idMensaje, fecha)
    else:
        idLogEvento=mbd.insertarLogEvento(con, idTipoLog, 0, idMensaje, fecha)
    con.close()
    logEvento= LogEvento(idLogEvento, tipoLogEvento, dispositivo, mensaje, fecha)
    if (tipoLogEvento.get_enviar_sms() == 'S'):
        print('ENVIAR SMS')
        sms= SMS()
        if sms.enviarSMS(logEvento) == 'F':
            idTipoLog= TiposLogs.errorSMS
            idMensaje= Mensajes.falloSMS
            generarLogEvento(idTipoLog, idMensaje, 0)
        """LLAMAR A METODO DE ENVIO DE SMS"""
    if (tipoLogEvento.get_enviar_mail() == 'S'):
        print('ENVIAR MAIL')
        """LLAMAR A METODO DE ENVIO DE MAIL POR WS"""

def cambiarPosicionActuadorAvance(actuadorAvance, nroDestino):
    """
    Método para cambiar de posicion un actuador de avance
    """
    posicionActual= actuadorAvance.get_posicion()
    if nroDestino > posicionActual:
        listaPosiciones= actuadorAvance.get_lista_posiciones()
        i= 0
        while i< len(listaPosiciones) and nroDestino <> listaPosiciones[i].get_posicion() :
            i= i+1
        if i < len(listaPosiciones):
            posicionDestino= listaPosiciones[i]
            listaSensores= posicionDestino.get_lista_sensores()
            ik= obtenerIkPadre (actuadorAvance)
            if ik <> None:
                tiempoInicial= time.time()
                expiroTiempo= False
                nroSaltos= nroDestino - posicionActual
                ik.setOutputState(actuadorAvance.get_numero_puerto(), 1) 
                detener= False
                while (detener == False):
                    control= True
                    j=0
                    while j<len(listaSensores) and control :
                        sensor= listaSensores[j]
                        j=j+1
                        lectura= lecturaSensor(sensor)
                        
                        tipoPuerto= sensor.get_tipo_puerto()
                        if tipoPuerto.get_nombre() == "analogico":
                            control= lectura == posicionDestino.get_valor()
                        else:
                            control= lectura
                    if control == True:
                        detener= True
                    tiempoActual= time.time()
                    diferenciaTiempo=int(tiempoActual-tiempoInicial)
                    if diferenciaTiempo >= (actuadorAvance.get_tiempo_entre_posiciones() * nroSaltos):
                        detener=True
                        expiroTiempo= True
                    
                ik.setOutputState(actuadorAvance.get_numero_puerto(), 0)
                if expiroTiempo:
                    print("Expiro el tiempo máximo para completar el movimiento")
                    idTipoLog= TiposLogs.expiroTiempoMovimiento
                    idMensaje= Mensajes.expiroTiempoPosiciones
                    generarLogEvento(idTipoLog, idMensaje, actuadorAvance)
                    return 'F'
                else:
                    actuadorAvance.set_posicion(nroDestino)
                    mbd= ManejadorBD()
                    con= mbd.getConexion()
                    mbd.cambiarPosicionActuadorAvance(con, actuadorAvance)
                    con.commit()
                    con.close()
                    return nroDestino
            else:
                print("No puede instanciar el padre")
                idTipoLog= TiposLogs.noSePuedeInstanciarPadre
                idMensaje= Mensajes.noSePuedeInstanciarPadre
                generarLogEvento(idTipoLog, idMensaje, actuadorAvance.get_padre())
                return 'F'
        else:
            print ("El actuador de avance no tiene esa posicion")
            return 'F'
    elif nroDestino < posicionActual:
        listaPosiciones= actuadorAvance.get_lista_posiciones()
        i= 0
        while i< len(listaPosiciones) and nroDestino <> listaPosiciones[i].get_posicion() :
            i= i+1
        if i < len(listaPosiciones):
            posicionDestino= listaPosiciones[i]
            listaSensores= posicionDestino.get_lista_sensores()
            ik= obtenerIkPadre (actuadorAvance)
            if ik <> None:
                tiempoInicial= time.time()
                expiroTiempo= False
                nroSaltos= posicionActual - nroDestino
                ik.setOutputState(actuadorAvance.get_numero_puerto_retroceso(), 1) 
                detener= False
                while (detener == False):
                    control= True
                    j=0
                    while j<len(listaSensores) and control :
                        sensor= listaSensores[j]
                        j= j+1
                        lectura= lecturaSensor(sensor)
                        tipoPuerto= sensor.get_tipo_puerto()
                        if tipoPuerto.get_nombre() == "analogico":
                            control= lectura == posicionDestino.get_valor()
                        else:
                            control= lectura
                    if control==True:
                        detener= True
                    tiempoActual= time.time()
                    diferenciaTiempo=int(tiempoActual-tiempoInicial)
                    
                    if diferenciaTiempo >= (actuadorAvance.get_tiempo_entre_posiciones() * nroSaltos):
                        detener=True
                        expiroTiempo= True
                ik.setOutputState(actuadorAvance.get_numero_puerto_retroceso(), 0)
                if expiroTiempo:
                    print("Expiro el tiempo máximo para completar el movimiento")
                    idTipoLog= TiposLogs.expiroTiempoMovimiento
                    idMensaje= Mensajes.expiroTiempoPosiciones
                    generarLogEvento(idTipoLog, idMensaje, actuadorAvance)
                    return 'F'
                else:
                    actuadorAvance.set_posicion(nroDestino)
                    mbd= ManejadorBD()
                    con= mbd.getConexion()
                    mbd.cambiarPosicionActuadorAvance(con, actuadorAvance)
                    con.commit()
                    con.close()
                    return nroDestino
            else:
                print("No puede instanciar el padre")
                idTipoLog= TiposLogs.noSePuedeInstanciarPadre
                idMensaje= Mensajes.noSePuedeInstanciarPadre
                generarLogEvento(idTipoLog, idMensaje, actuadorAvance.get_padre())
                return 'F'
        else:
            print ("El actuador de avance no tiene esa posicion")
            return 'F'
            
def cambiarPosicionGrupoActuadores(grupo, nroPosicion):
    """
    Método para apagar un grupo de actuadores
    """
    listaAcciones= list()
    listaActuadores= grupo.get_lista_actuadores()
    for actuadorAvance in listaActuadores:
        posicionActual= actuadorAvance.get_posicion()
        if posicionActual <> nroPosicion:
            estadoActuador=cambiarPosicionActuadorAvance(actuadorAvance, nroPosicion)
            if estadoActuador == 'F':
                print('ERROR CAMBIO POSICIÓN ACTUADOR')
            else:
                mbd= ManejadorBD()
                con= mbd.getConexion()
                idActuador= actuadorAvance.get_id_dispositivo()
                mbd.insertarAccionActuador(con, idActuador, str(estadoActuador))
                con.commit()
                con.close()
            listaAcciones.append(estadoActuador)
    if len(listaAcciones) == 0:
        #todos los actuadores ya estaban en la posicion destino
        idMensaje=Mensajes.actuadoresEnPosicion
    else:
        error= True
        i=0
        while i<len(listaAcciones) and error:
            error= listaAcciones[i] == 'F'
            i= i+1
        if error == True:
            #falló el movimiento de todos los dispositivos
            idMensaje= Mensajes.movimientoGrupoError
        else:
            exito= True
            i=0
            while i<len(listaAcciones) and exito:
                exito= listaAcciones[i] == nroPosicion
                i= i+1
            if exito == True:
                #se acambio la posición de todos los dispositivos del grupo de actuadores
                idMensaje= Mensajes.movimientoGrupoOk
                grupo.set_estado(str(nroPosicion))
                mbd= ManejadorBD()
                con= mbd.getConexion()
                mbd.cambiarEstadoGrupoActuadores(con, grupo)
                con.commit()
                con.close()
            else:
                #el grupo de actuadores cambió de posición parcialmente
                idMensaje=Mensajes.movimientoGrupoParcial
                grupo.set_estado(str(nroPosicion))
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

def iniciarHiloWS():
    t = iniciarWS()
    t.start()
    print("WS publicado")
    
def iniciarHiloLecturas():    
    t2= tomarLecturas()
    t2.start()
    print('Lecturas automáticas iniciadas')
    
def iniciarHiloNiveles():        
    t3= procesarNiveles()
    t3.start()
    print('Procesado niveles iniciado')

class Comunicacion(SimpleWSGISoapApp):
    
    @soapmethod(Integer,_returns=ResultadoAccionWS)
    def wsEncenderGrupoActuadores(self, idGrupo):
        placa= getPlaca()
        estadoSistema= placa.get_estado_sistema()
        if estadoSistema == 'M':
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
        else:
            idMensaje= Mensajes.estadoSistemaNoEsManual
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
        estadoSistema= placa.get_estado_sistema()
        if estadoSistema == 'M':
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
        else:
            idMensaje= Mensajes.estadoSistemaNoEsManual
            mbd= ManejadorBD()
            con= mbd.getConexion()
            mensaje=mbd.obtenerMensaje(con, idMensaje)
            con.close()
            fecha= datetime.now()
            tipoAccion= ""
            resultadoWS= ResultadoAccionWS(mensaje, fecha, idGrupo, tipoAccion)
        return resultadoWS
    
    @soapmethod(Integer, Integer,_returns=ResultadoAccionWS)
    def wsCambiarPosicionGrupoActuadores(self, idGrupo, nroPosicion):
        placa= getPlaca()
        estadoSistema= placa.get_estado_sistema()
        if estadoSistema == 'M':
            listaGrupoActuadores= placa.get_lista_grupo_actuadores()
            mensaje= None
            grupo=None
        
            i=0
            while i < len(listaGrupoActuadores) and idGrupo <> listaGrupoActuadores[i].get_id_grupo_actuador():
                i= i+1
            if i < len(listaGrupoActuadores):
                grupo= listaGrupoActuadores[i]
                resultado=cambiarPosicionGrupoActuadores(grupo, nroPosicion)
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
        else:
            idMensaje= Mensajes.estadoSistemaNoEsManual
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
        estadoSistema= placa.get_estado_sistema()
        if estadoSistema == 'M' or estadoSistema == 'A':
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
        else:
            idMensaje= Mensajes.estadoSistemaNoManualNiAutomatico
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
    
    @soapmethod(String, String, Integer, Integer, Integer, _returns=ResultadoCreacionWS)
    def wsCrearFactor(self, nombre, unidad, valorMin, valorMax, umbral):
        placa= getPlaca()
        estadoSistema= placa.get_estado_sistema()
        if estadoSistema == 'C':
            idFactor= crearFactor(nombre, unidad, valorMin, valorMax, umbral)
            idMensaje= Mensajes.factorCreadoOk
            mbd= ManejadorBD()
            con= mbd.getConexion()
            mensaje=mbd.obtenerMensaje(con, idMensaje)
            con.close()
        else:
            idMensaje= Mensajes.estadoActualNoEsConfiguracion
            mbd= ManejadorBD()
            con= mbd.getConexion()
            mensaje=mbd.obtenerMensaje(con, idMensaje)
            con.close()
        resultado= ResultadoCreacionWS(mensaje, idFactor)
        return resultado
    
    @soapmethod(String, String, _returns=ResultadoCreacionWS)
    def wsCrearGrupoActuadores(self, nombre, deAvance):
        placa= getPlaca()
        estadoSistema= placa.get_estado_sistema()
        if estadoSistema == 'C':
            idGrupo= crearGrupoActuadores(nombre, deAvance)
            idMensaje= Mensajes.grupoActuadoresCreadoOk
            mbd= ManejadorBD()
            con= mbd.getConexion()
            mensaje=mbd.obtenerMensaje(con, idMensaje)
            con.close()
        else:
            idMensaje= Mensajes.estadoActualNoEsConfiguracion
            mbd= ManejadorBD()
            con= mbd.getConexion()
            mensaje=mbd.obtenerMensaje(con, idMensaje)
            con.close()
        resultado= ResultadoCreacionWS(mensaje, idGrupo)
        return resultado
    
    @soapmethod(String, String, Integer, String, Integer, Integer, Integer, _returns=ResultadoCreacionWS)
    def wsCrearSensor(self, nombre, modelo, nroPuerto, formulaConversion, idTipoPuerto, idPlacaPadre, idFactor):
        placa= getPlaca()
        estadoSistema= placa.get_estado_sistema()
        if estadoSistema == 'C':
            idSensor= crearSensor(nombre, modelo, nroPuerto, formulaConversion, idTipoPuerto, idPlacaPadre, idFactor)
            idMensaje= Mensajes.sensorCreadoOk
            mbd= ManejadorBD()
            con= mbd.getConexion()
            mensaje=mbd.obtenerMensaje(con, idMensaje)
            con.close()
        else:
            idMensaje= Mensajes.estadoActualNoEsConfiguracion
            mbd= ManejadorBD()
            con= mbd.getConexion()
            mensaje=mbd.obtenerMensaje(con, idMensaje)
            con.close()
        resultado= ResultadoCreacionWS(mensaje, idSensor)
        return resultado
    
    @soapmethod(String,String, Integer, Integer, Integer, Integer, Integer, _returns=ResultadoCreacionWS)
    def wsCrearActuador(self, nombre, modelo, nroPuerto, idTipoPuerto, idTipoActuador, idPlacaPadre, idGrupoActuadores):
        placa= getPlaca()
        estadoSistema= placa.get_estado_sistema()
        idActuador= 0
        if estadoSistema == 'C':
            idActuador= crearActuador(nombre, modelo, nroPuerto, idTipoPuerto, idTipoActuador, idPlacaPadre, idGrupoActuadores)
            idMensaje= Mensajes.actuadorCreadoOk
            mbd= ManejadorBD()
            con= mbd.getConexion()
            mensaje=mbd.obtenerMensaje(con, idMensaje)
            con.close()
        else:
            idMensaje= Mensajes.estadoActualNoEsConfiguracion
            mbd= ManejadorBD()
            con= mbd.getConexion()
            mensaje=mbd.obtenerMensaje(con, idMensaje)
            con.close()
        resultado= ResultadoCreacionWS(mensaje, idActuador)
        return resultado
    
    @soapmethod(String, _returns=ResultadoCreacionWS)
    def wsCrearTipoPlaca(self, nombre):
        placa= getPlaca()
        estadoSistema= placa.get_estado_sistema()
        if estadoSistema == 'C':
            idTipoPlaca= crearTipoPlaca(nombre)
            idMensaje= Mensajes.tipoPlacaCreadaOk
            mbd= ManejadorBD()
            con= mbd.getConexion()
            mensaje=mbd.obtenerMensaje(con, idMensaje)
            con.close()
        else:
            idMensaje= Mensajes.estadoActualNoEsConfiguracion
            mbd= ManejadorBD()
            con= mbd.getConexion()
            mensaje=mbd.obtenerMensaje(con, idMensaje)
            con.close()
        resultado= ResultadoCreacionWS(mensaje, idTipoPlaca)
        return resultado
    
    @soapmethod(String, _returns=ResultadoCreacionWS)
    def wsCrearTipoActuador(self, nombre):
        placa= getPlaca()
        estadoSistema= placa.get_estado_sistema()
        if estadoSistema == 'C':
            idTipoActuador= crearTipoActuador(nombre)
            idMensaje= Mensajes.tipoActuadorCreadoOk
            mbd= ManejadorBD()
            con= mbd.getConexion()
            mensaje=mbd.obtenerMensaje(con, idMensaje)
            con.close()
        else:
            idMensaje= Mensajes.estadoActualNoEsConfiguracion
            mbd= ManejadorBD()
            con= mbd.getConexion()
            mensaje=mbd.obtenerMensaje(con, idMensaje)
            con.close()
        resultado= ResultadoCreacionWS(mensaje, idTipoActuador)
        return resultado
    
    @soapmethod(String,String, Integer, String, Integer, Integer, _returns=ResultadoCreacionWS)
    def wsCrearPlacaAuxiliar(self, nombre, modelo, nroPuerto, nroSerie, idTipoPlaca, idPlacaPadre):
        placa= getPlaca()
        estadoSistema= placa.get_estado_sistema()
        if estadoSistema == 'C':
            idPlacaAuxiliar= crearPlacaAuxiliar(nombre, modelo, nroPuerto, nroSerie, idTipoPlaca, idPlacaPadre)
            idMensaje= Mensajes.placaAuxiliarCreadaOk
            mbd= ManejadorBD()
            con= mbd.getConexion()
            mensaje=mbd.obtenerMensaje(con, idMensaje)
            con.close()
        else:
            idMensaje= Mensajes.estadoActualNoEsConfiguracion
            mbd= ManejadorBD()
            con= mbd.getConexion()
            mensaje=mbd.obtenerMensaje(con, idMensaje)
            con.close()
        resultado= ResultadoCreacionWS(mensaje, idPlacaAuxiliar)
        return resultado
    
    @soapmethod(String, Integer, Integer, Integer, Integer, _returns=ResultadoCreacionWS)
    def wsCrearNivelSeveridad(self, nombre, idFactor, prioridad, rangoMinimo, rangoMaximo):
        placa= getPlaca()
        estadoSistema= placa.get_estado_sistema()
        if estadoSistema == 'C':
            idNivel= crearNivelSeveridad(nombre, idFactor, prioridad, rangoMinimo, rangoMaximo)
            idMensaje= Mensajes.nivelSeveridadCreadoOk
            mbd= ManejadorBD()
            con= mbd.getConexion()
            mensaje=mbd.obtenerMensaje(con, idMensaje)
            con.close()
        else:
            idMensaje= Mensajes.estadoActualNoEsConfiguracion
            mbd= ManejadorBD()
            con= mbd.getConexion()
            mensaje=mbd.obtenerMensaje(con, idMensaje)
            con.close()
        resultado= ResultadoCreacionWS(mensaje, idNivel)
        return resultado
    
    @soapmethod(Integer, Integer, String, _returns=ResultadoCreacionWS)
    def wsAgregarFilaPerfilActivacion(self, idPerfilActivacion, idGrupoActuadores, estado):
        placa= getPlaca()
        estadoSistema= placa.get_estado_sistema()
        if estadoSistema == 'C':
            agregarFilaPerfilActivacion(idPerfilActivacion, idGrupoActuadores, estado)
            idMensaje= Mensajes.filaPerfilActivacionAgregadaOk
            mbd= ManejadorBD()
            con= mbd.getConexion()
            mensaje=mbd.obtenerMensaje(con, idMensaje)
            con.close()
        else:
            idMensaje= Mensajes.estadoActualNoEsConfiguracion
            mbd= ManejadorBD()
            con= mbd.getConexion()
            mensaje=mbd.obtenerMensaje(con, idMensaje)
            con.close()
        resultado= ResultadoCreacionWS(mensaje, idPerfilActivacion)
        return resultado
    
    @soapmethod(String,String, Integer, Integer, Integer, Integer, Integer, Integer, Integer, Integer, Integer, _returns=ResultadoCreacionWS)
    def wsCrearActuadorAvance(self, nombre, modelo, nroPuerto, posicion, idTipoPuerto, idTipoActuador, idPlacaPadre, nroPuertoRetroceso, tipoPuertoRetroceso, tiempoEntrePosiciones, idGrupoActuadores):
        placa= getPlaca()
        estadoSistema= placa.get_estado_sistema()
        if estadoSistema == 'C':
            idActuadorAvance= crearActuadorAvance(nombre, modelo, nroPuerto, posicion, idTipoPuerto, idTipoActuador, idPlacaPadre, nroPuertoRetroceso, tipoPuertoRetroceso, tiempoEntrePosiciones, idGrupoActuadores)
            idMensaje= Mensajes.actuadorAvanceCreadoOk
            mbd= ManejadorBD()
            con= mbd.getConexion()
            mensaje=mbd.obtenerMensaje(con, idMensaje)
            con.close()
        else:
            idMensaje= Mensajes.estadoActualNoEsConfiguracion
            mbd= ManejadorBD()
            con= mbd.getConexion()
            mensaje=mbd.obtenerMensaje(con, idMensaje)
            con.close()
        resultado= ResultadoCreacionWS(mensaje, idActuadorAvance)
        return resultado
    
    @soapmethod(Integer, Integer, String, Integer, _returns=ResultadoCreacionWS)
    def wsAgregarPosicionActuadorAvance(self, idActuadorAvance, numeroPosicion, descripcion, valor):
        placa= getPlaca()
        estadoSistema= placa.get_estado_sistema()
        if estadoSistema == 'C':
            agregarPosicionActuadorAvance(idActuadorAvance, numeroPosicion, descripcion, valor)
            idMensaje= Mensajes.posicionActuadorAvanceOk
            mbd= ManejadorBD()
            con= mbd.getConexion()
            mensaje=mbd.obtenerMensaje(con, idMensaje)
            con.close()
        else:
            idMensaje= Mensajes.estadoActualNoEsConfiguracion
            mbd= ManejadorBD()
            con= mbd.getConexion()
            mensaje=mbd.obtenerMensaje(con, idMensaje)
            con.close()
        resultado= ResultadoCreacionWS(mensaje, numeroPosicion)
        return resultado
    
    @soapmethod(Integer, Integer, Integer, _returns=ResultadoCreacionWS)
    def wsAgregarSensorPosicionActuadorAvance(self, idSensor, idActuadorAvance, numeroPosicion):
        placa= getPlaca()
        estadoSistema= placa.get_estado_sistema()
        if estadoSistema == 'C':
            agregarSensorPosicionActuadorAvance(idSensor, idActuadorAvance, numeroPosicion)
            idMensaje= Mensajes.sensorPosicionActuadorAvanceOk
            mbd= ManejadorBD()
            con= mbd.getConexion()
            mensaje=mbd.obtenerMensaje(con, idMensaje)
            con.close()
        else:
            idMensaje= Mensajes.estadoActualNoEsConfiguracion
            mbd= ManejadorBD()
            con= mbd.getConexion()
            mensaje=mbd.obtenerMensaje(con, idMensaje)
            con.close()
        resultado= ResultadoCreacionWS(mensaje, idSensor)
        return resultado
    
    @soapmethod(Integer, _returns=Mensaje)
    def wsEliminarDispositivo(self, idDispositivo):
        placa= getPlaca()
        estadoSistema= placa.get_estado_sistema()
        if estadoSistema == 'C':
            eliminarDispositivo(idDispositivo)
            idMensaje= Mensajes.dispositivoEliminadoOk
            mbd= ManejadorBD()
            con= mbd.getConexion()
            mensaje=mbd.obtenerMensaje(con, idMensaje)
            con.close()
        else:
            idMensaje= Mensajes.estadoActualNoEsConfiguracion
            mbd= ManejadorBD()
            con= mbd.getConexion()
            mensaje=mbd.obtenerMensaje(con, idMensaje)
            con.close()
        return mensaje
    
    @soapmethod(Integer, _returns=Mensaje)
    def wsEliminarFactor(self, idFactor):
        placa= getPlaca()
        estadoSistema= placa.get_estado_sistema()
        if estadoSistema == 'C':
            eliminarFactor(idFactor)
            idMensaje= Mensajes.factorEliminadoOk
            mbd= ManejadorBD()
            con= mbd.getConexion()
            mensaje=mbd.obtenerMensaje(con, idMensaje)
            con.close()
        else:
            idMensaje= Mensajes.estadoActualNoEsConfiguracion
            mbd= ManejadorBD()
            con= mbd.getConexion()
            mensaje=mbd.obtenerMensaje(con, idMensaje)
            con.close()
        return mensaje
    
    @soapmethod(Integer, _returns=Mensaje)
    def wsEliminarGrupoActuadores(self, idGrupoActuadores):
        placa= getPlaca()
        estadoSistema= placa.get_estado_sistema()
        if estadoSistema == 'C':
            eliminarGrupoActuadores(idGrupoActuadores)
            idMensaje= Mensajes.grupoActuadoresEliminadoOk
            mbd= ManejadorBD()
            con= mbd.getConexion()
            mensaje=mbd.obtenerMensaje(con, idMensaje)
            con.close()
        else:
            idMensaje= Mensajes.estadoActualNoEsConfiguracion
            mbd= ManejadorBD()
            con= mbd.getConexion()
            mensaje=mbd.obtenerMensaje(con, idMensaje)
            con.close()
        return mensaje
    
    @soapmethod(Integer, _returns=Mensaje)
    def wsEliminarNivelSeveridad(self, idNivelSeveridad):
        placa= getPlaca()
        estadoSistema= placa.get_estado_sistema()
        if estadoSistema == 'C':
            eliminarNivelSeveridad(idNivelSeveridad)
            idMensaje= Mensajes.nivelSeveridadEliminadoOk
            mbd= ManejadorBD()
            con= mbd.getConexion()
            mensaje=mbd.obtenerMensaje(con, idMensaje)
            con.close()
        else:
            idMensaje= Mensajes.estadoActualNoEsConfiguracion
            mbd= ManejadorBD()
            con= mbd.getConexion()
            mensaje=mbd.obtenerMensaje(con, idMensaje)
            con.close()
        return mensaje
    
    @soapmethod(Integer, Integer, _returns=Mensaje)
    def wsEliminarFilaPerfilActivacion(self, idPerfil, idGrupoActuadores):
        placa= getPlaca()
        estadoSistema= placa.get_estado_sistema()
        if estadoSistema == 'C':
            eliminarFilaPerfilActivacion(idPerfil, idGrupoActuadores)
            idMensaje= Mensajes.filaPerfilActivacionEliminadoOk
            mbd= ManejadorBD()
            con= mbd.getConexion()
            mensaje=mbd.obtenerMensaje(con, idMensaje)
            con.close()
        else:
            idMensaje= Mensajes.estadoActualNoEsConfiguracion
            mbd= ManejadorBD()
            con= mbd.getConexion()
            mensaje=mbd.obtenerMensaje(con, idMensaje)
            con.close()
        return mensaje

if __name__ == '__main__':
    __placa=iniciarPlaca()
    if __placa <> None:
        iniciarHiloWS()
        estado= __placa.get_estado_sistema()
        if estado == 'M' or estado == 'A':
            iniciarHiloLecturas()
        if estado == 'A':
            iniciarHiloNiveles()
    else:
        print('Sistema finalizado...')
