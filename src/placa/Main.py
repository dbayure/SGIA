# -*- encoding: utf-8 -*-
"""
Módulo principal del sistema, es el encargado de iniciar la ejecución del mismo.
Debe instanciar la placa y el servidor de WS, además es encargado de comunicarse con la capa de persistencia para guardar y recuperar datos.
Tiene como atributos una instancia única de placa y una instancia única de WS.
"""
from src.placa.Placa import Placa
from src.recursos.Herramientas import Herramientas
from src.placa.PlacaAuxiliar import PlacaAuxiliar
from src.recursos import Propiedades, TiposLogs, Mensajes
from src.lecturas.ResultadoLectura import ResultadoLectura
from datetime import datetime
from src.lecturas.ResultadoAccion import ResultadoAccion
from src.logs.Mensaje import Mensaje
from src.bdd.ManejadorBD import ManejadorBD
from soaplib.wsgi_soap import SimpleWSGISoapApp
from soaplib.service import soapmethod
from soaplib.serializers.primitive import String, Integer
import threading
from src.ws.ResultadoLecturaWS import ResultadoLecturaWS
from src.ws.ResultadoAccionWS import ResultadoAccionWS
from src.ws.ResultadoCreacionWS import ResultadoCreacionWS
from src.ws.ResultadoDatosPlacaWS import ResultadoDatosPlacaWS
import time
import math
from src.placa.ActuadorAvance import ActuadorAvance
from src.logs.LogEvento import LogEvento
from src.logs.SMS import SMS
from src.logs.SendLectura import SendLectura

__placa=None
__ws=None

def iniciarPlaca():
    """Método para inicializar la placa controladora y cargar sus estructuras desde la BD
    @rtype: Placa
    @return: Devuelve la instancia única de la placa con todas sus estructuras cargadas"""
    mbd= ManejadorBD()
    con= mbd.getConexion()
    estadoSistema= mbd.obtenerEstadoPlaca(con)
    nroSerie= mbd.obtenerNroSeriePlaca(con)
    periodicidadLecturas= mbd.obtenerPeriodicidadLecturasPlaca(con)
    periodicidadNiveles= mbd.obtenerPeriodicidadNivelesPlaca(con)
    listaDispositivos= mbd.obtenerListaDispositivos(con)
    listaFactores= mbd.obtenerListaFactores(con)
    estadoAlerta= mbd.obtenerEstadoAlertaSistema(con)
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
        placa= Placa(nroSerie, estadoSistema, periodicidadLecturas, periodicidadNiveles, listaDispositivos, listaGrupoActuadores, listaFactores, listaNivelesSeveridad, estadoAlerta) 
        placa.set_ik(ik)
        chequearPlacasAuxiliares(listaDispositivos)
    else:
        print('ERROR FATAL')
        idTipoLog= TiposLogs.noSePuedeInstanciarPC
        idMensaje= Mensajes.noSePuedeInstanciarPlacaControladora            
        generarLogEvento(idTipoLog, idMensaje, 0)
    return placa

def chequearPlacasAuxiliares(listaDispositivos):
    """Método que permite verificar que todas las placas auxiliares del sistema hayan podidio instanciar su objeto IK, y en caso contrario emitir el LogEvento, y actualizar su estado de alerta."""
    for dispositivo in listaDispositivos:
        if isinstance(dispositivo, (PlacaAuxiliar)):
            if dispositivo.get_ik() == None and dispositivo.get_estado_alerta() == 'N':
                idTipoLog= TiposLogs.noSePuedeInstanciarPlacaAuxiliar
                idMensaje= Mensajes.noSePuedeInstanciarPlacaAuxiliar
                generarLogEvento(idTipoLog, idMensaje, dispositivo)
                mbd= ManejadorBD()
                con= mbd.getConexion()
                mbd.cambiarEstadoAlerta(con, dispositivo.get_id_dispositivo(), 'S')
                con.close()
            elif dispositivo.get_ik() <> None and dispositivo.get_estado_alerta() == 'S':
                idTipoLog= TiposLogs.placaAuxiliarRecuperada
                idMensaje= Mensajes.dispositivoRecuperado
                generarLogEvento(idTipoLog, idMensaje, dispositivo)
                mbd= ManejadorBD()
                con= mbd.getConexion()
                mbd.cambiarEstadoAlerta(con, dispositivo.get_id_dispositivo(), 'N')
                con.close()
            chequearPlacasAuxiliares(dispositivo.get_lista_dispositivos())

def obtenerDispositivoSegunId(listaDispositivos, idDispositivo):
    """Método para buscar y recuperar un dispositivo instanciado en el sistema dado su identificador.
    @rtype: Dispositivo
    @return: Devuelve el objeto Dispositivo al que corresponde el idDispositivo pasado como parámetro""" 
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


def obtenerDatosPlaca():
    mbd= ManejadorBD()
    con= mbd.getConexion()
    datosPlaca=mbd.obtenerDatosPlaca(con)
    con.close()
    return datosPlaca

def obtenerEstadoAlertaSistema():
    mbd= ManejadorBD()
    con= mbd.getConexion()
    estadoSistema=mbd.obtenerEstadoAlertaSistema(con)
    con.close()
    return estadoSistema

def obtenerEstadoAlertaDispostivo(idDispositivo):
    mbd= ManejadorBD()
    con= mbd.getConexion()
    estadoDispositivo=mbd.obtenerEstadoAlertaDispositivo(con, idDispositivo)
    con.close()
    return estadoDispositivo

class iniciarWS(threading.Thread):
    """Clase que extiende threading.Thread, utilizada para publicar el WS como un nuevo hilo de ejecución del sistema."""
    def __init__(self):
        threading.Thread.__init__(self)
    
    def run(self):
        """Método al que debe invocarse para poner al hilo en ejecución"""
        try:
            from wsgiref.simple_server import make_server
            mbd= ManejadorBD()
            con= mbd.getConexion()
            hostPuerto= mbd.obtenerHostPuertoWS(con)
            server = make_server(hostPuerto[0], int(hostPuerto[1]), Comunicacion())
            server.serve_forever()
        except:
            print ("Error al iniciar WS")
            
class tomarLecturas(threading.Thread):
    """Clase que extiende threading.Thread, utilizada iniciar las lecturas automáticas de factores como un nuevo hilo de ejecución del sistema."""
    def __init__(self):
        threading.Thread.__init__(self)
    
    def run(self):
        """Método al que debe invocarse para poner al hilo en ejecución"""
        placa= getPlaca()
        listaFactores= placa.get_lista_factores()
        while (placa.get_estado_sistema() == 'A' or placa.get_estado_sistema() == 'M'):
            for factor in listaFactores:
                procesarLecturaFactor(factor)
            time.sleep(placa.get_periodicidad_lecturas())
            
class enviarLecturas(threading.Thread):
    """Clase que extiende threading.Thread, utilizada enviar las lecturas obtenidas por los sensores como un nuevo hilo de ejecución del sistema."""
    def __init__(self):
        threading.Thread.__init__(self)
    
    def run(self):
        """Método al que debe invocarse para poner al hilo en ejecución"""
        print('entra a informar')
        placa= getPlaca()
        listaFactores= placa.get_lista_factores()
        numeroLecturas= Propiedades.factorInformeLecturas * Propiedades.factorRecuperacion
        mbd= ManejadorBD()
        con= mbd.getConexion()
        datosAC= mbd.obtenerHostPuertoWS_Centralizadora(con)
        con.close()
        sendLec= SendLectura(datosAC[0], datosAC[1])
        while (placa.get_estado_sistema() == 'A' or placa.get_estado_sistema() == 'M'):
            for factor in listaFactores:
                con= mbd.getConexion()
                listaLecturasFactor= mbd.obtenerListaLecturasFactorCantidad(con, factor.get_id_factor(), numeroLecturas)
                con.close()
                ok=sendLec.enviarLecturasFactor(placa.get_nro_serie(), listaLecturasFactor)
                if (ok):
                    con= mbd.getConexion()
                    for l in listaLecturasFactor:
                        con= mbd.getConexion()
                        mbd.marcarLecturaFactorInformada(con, l.get_id_lectura())
                    con.close()
                listaSensores=factor.get_lista_sensores()
                for sensor in listaSensores:
                    con= mbd.getConexion()
                    listaLecturas= mbd.obtenerLecturasSensorCantidad(con, sensor.get_id_dispositivo(), numeroLecturas)
                    con.close()
                    ok=sendLec.enviarLecturas(placa.get_nro_serie(), listaLecturas)
                    if (ok):
                        con= mbd.getConexion()
                        for l in listaLecturas:
                            con= mbd.getConexion()
                            mbd.marcarLecturaInformada(con, l.get_id_lectura())
                        con.close()
            time.sleep( placa.get_periodicidad_lecturas() * Propiedades.factorInformeLecturas)
            
class enviarAcciones(threading.Thread):
    """Clase que extiende threading.Thread, utilizada enviar las lecturas obtenidas por los sensores como un nuevo hilo de ejecución del sistema."""
    def __init__(self):
        threading.Thread.__init__(self)
    
    def run(self):
        """Método al que debe invocarse para poner al hilo en ejecución"""
        print('entra a informar')
        placa= getPlaca()
        listaGruposActuadores= placa.get_lista_grupo_actuadores()
        numeroAcciones= Propiedades.factorInformeLecturas * Propiedades.factorRecuperacion
        mbd= ManejadorBD()
        con= mbd.getConexion()
        datosAC= mbd.obtenerHostPuertoWS_Centralizadora(con)
        con.close()
        sendLec= SendLectura(datosAC[0], datosAC[1])
        while (placa.get_estado_sistema() == 'A' or placa.get_estado_sistema() == 'M'):
            for grupo in listaGruposActuadores:
                
                listaActuadores=grupo.get_lista_actuadores()
                for actuador in listaActuadores:
                    con= mbd.getConexion()
                    listaAcciones= mbd.obtenerAccionesCantidad(con, actuador.get_id_dispositivo(), numeroAcciones)
                    con.close()
                    if (len(listaAcciones) > 0):
                        ok=sendLec.enviarAcciones(placa.get_nro_serie(), listaAcciones)
                        if (ok):
                            con= mbd.getConexion()
                            for a in listaAcciones:
                                con= mbd.getConexion()
                                mbd.marcarAccionInformada(con, a.get_id_accion())
                            con.close()
            time.sleep( placa.get_periodicidad_lecturas() * Propiedades.factorInformeLecturas)
            
class enviarLogEventos(threading.Thread):
    """Clase que extiende threading.Thread, utilizada enviar las lecturas obtenidas por los sensores como un nuevo hilo de ejecución del sistema."""
    def __init__(self):
        threading.Thread.__init__(self)
    
    def run(self):
        """Método al que debe invocarse para poner al hilo en ejecución"""
        print('entra a informar log de eventos')
        placa= getPlaca()
        numeroLogs= Propiedades.factorInformeLecturas * Propiedades.factorRecuperacion
        mbd= ManejadorBD()
        con= mbd.getConexion()
        datosAC= mbd.obtenerHostPuertoWS_Centralizadora(con)
        con.close()
        sendLec= SendLectura(datosAC[0], datosAC[1])
        while (placa.get_estado_sistema() == 'A' or placa.get_estado_sistema() == 'M'):
            
            con= mbd.getConexion()
            listaLogs= mbd.obtenerLogEventosCantidad(con, numeroLogs)
            con.close()
            if (len(listaLogs)>0):
                ok=sendLec.enviarLogEventoPendientes(placa.get_nro_serie(), listaLogs)
                if (ok):
                    con= mbd.getConexion()
                    for l in listaLogs:
                        con= mbd.getConexion()
                        mbd.marcarLogEventoInformada(con, l.get_id_log_evento())
                    con.close()
            time.sleep( placa.get_periodicidad_lecturas() * Propiedades.factorInformeLecturas)
            
class estadoAlertaSistema(threading.Thread):
    """Clase que extiende threading.Thread, utilizada iniciar el análisis de estado de alerta del sistema como un nuevo hilo de ejecución."""
    def __init__(self):
        threading.Thread.__init__(self)
    
    def run(self):
        """Método al que debe invocarse para poner al hilo en ejecución"""
        placa= getPlaca()
        while (placa.get_estado_sistema() == 'A' or placa.get_estado_sistema() == 'M'):
            mbd= ManejadorBD()
            con= mbd.getConexion()
            cantEstadoAlerta=mbd.obtenerCantidadDispositivosAlerta(con)
            if cantEstadoAlerta == 0:
                placa.set_estado_alerta('N')
                con= mbd.getConexion()
                mbd.cambiarEstadoAlertaSistema(con, 'N')
                con.commit()
                con.close()
            else:
                placa.set_estado_alerta('S')
                con= mbd.getConexion()
                mbd.cambiarEstadoAlertaSistema(con, 'S')
                con.commit()
                con.close()
            time.sleep(placa.get_periodicidad_lecturas())
            
class procesarEstadoAlertaSistema(threading.Thread):
    """Clase que extiende threading.Thread, utilizada iniciar el procesado de estado de alerta del sistema y la emisión de notificaciones visuales como un nuevo hilo de ejecución."""
    def __init__(self):
        threading.Thread.__init__(self)
    
    def run(self):
        """Método al que debe invocarse para poner al hilo en ejecución"""
        placa= getPlaca()
        ik= placa.get_ik()
        while (placa.get_estado_sistema() == 'A' or placa.get_estado_sistema() == 'M'):
            i= 1
            while (placa.get_estado_alerta() == 'S'):
                ik.setOutputState((i-1), 0)
                ik.setOutputState(i, 1)
                time.sleep(2)
                if i == 3:
                    ik.setOutputState(3, 0)
                    i= 1
                else:
                    i= i+1
            if (placa.get_estado_sistema() == 'A' or placa.get_estado_sistema() == 'M'):
                ik.setOutputState(0, 1)
                time.sleep(1)
                ik.setOutputState(1, 0)
                time.sleep(1)
                ik.setOutputState(2, 0)
                time.sleep(1)
                ik.setOutputState(3, 0)
            
class procesarNiveles(threading.Thread):
    """Clase que extiende threading.Thread, utilizada iniciar el procesado de niveles de severidad  de forma automática, como un nuevo hilo de ejecución del sistema."""
    def __init__(self):
        threading.Thread.__init__(self)
    
    def run(self):
        """Método al que debe invocarse para poner al hilo en ejecución"""
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
                for nivel in listaNivelesValidos:
                    print("Nivel valido: "+nivel.get_nombre()+"; prioridad: "+str(nivel.get_prioridad()))
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
                """YA TENGO TODO LO NECESARIO PARA ACTUAR SOBRE LOS GRUPOS DE ACTUADORES SEGÚN SE HAYA ESPECIFICADO EN EL PERFIL DE ACTIVACION DE CADA NIVEL DE SEVERIDAD QUE SE ESTÁ CUMPLIENDO"""
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
                            print ("Estado no valido para perfil de activación")
                            
def iniciarHiloWS():
    """Método para iniciar WS como hilo secundario del sistema"""
    t = iniciarWS()
    t.start()
    print("WS publicado")
    
def iniciarHiloLecturas():  
    """Método para iniciar el procesado de lecturas automático como hilo secundario del sistema"""  
    t2= tomarLecturas()
    t2.start()
    print('Lecturas automaticas iniciadas')
    
def iniciarHiloNiveles():      
    """Método para iniciar el procesado de niveles de severidad automático como hilo secundario del sistema"""    
    t3= procesarNiveles()
    t3.start()
    print('Procesado niveles iniciado')
    
def iniciarHiloEstadoAlertaSistema():  
    """Método para iniciar el análisis del estado de alerta del sistema como hilo secundario del mismo"""        
    t4= estadoAlertaSistema()
    t4.start()
    print('Analisis estado alerta sistema iniciado')
    
def iniciarHiloProcesarEstadoAlertaSistema(): 
    """Método para iniciar el procesado del estado de alerta del sistema y activación de notificaciones visuales, como hilo secundario del sistema"""      
    t5= procesarEstadoAlertaSistema()
    t5.start()
    print('Procesado estado alerta sistema iniciado')
    
def iniciarHiloInformeLecturas(): 
    """Método para iniciar el procesado de envio de lecturas obtenidas, como hilo secundario del sistema"""      
    t6= enviarLecturas()
    t6.start()
    print('Informe de lecturas iniciado')
    
def iniciarHiloInformeAcciones(): 
    """Método para iniciar el procesado de envio de acciones disparadas, como hilo secundario del sistema"""      
    t7= enviarAcciones()
    t7.start()
    print('Informe de lecturas iniciado')
    
def iniciarHiloInformeLogEventos(): 
    """Método para iniciar el procesado de envio de log de eventos disparadas, como hilo secundario del sistema"""      
    t8= enviarLogEventos()
    t8.start()
    print('Informe de log de eventos iniciado')
            
def analizarCumplimientoNivel( listaValoresLecturas, minimo, maximo):
    """Método para analizar si cumplen las condiciones que determinan el cumplimiento de un nivel de severidad.
    @param listaValoresLecturas: Lista de las últimas lecturas del factor asociado al nivel de severidad
    @param minimo: Rango mínimo de cumplimiento del nivel de severidad
    @param maximo: Rango máximo de cumplimiento del nivel de severidad
    @rtype: boolean
    @return: Devuelve si se cumple el nivel según los parámetros recibidos"""
    cantidadLecturas= len(listaValoresLecturas)
    objetivoLecturas= int((Propiedades.porcentajeLecturasProcNiveles * cantidadLecturas) / 100)
    coincidencias= 0
    for lectura in listaValoresLecturas:
        if lectura >= minimo and lectura < maximo:
            coincidencias= coincidencias +1 
    cumple= coincidencias >= objetivoLecturas
    return cumple  

def apagarTodo():
    """Método utilizado para apagar todos los dispositivos actuadores del sistema, y los elementos de alertas visuales"""
    listaGruposActuadores= __placa.get_lista_grupo_actuadores()
    for grupoActuadores in listaGruposActuadores:
        if grupoActuadores.get_de_avance() == 'N':
            apagarGrupoActuadores(grupoActuadores)
    ik= __placa.get_ik()
    ik.setOutputState(0, 0)
    ik.setOutputState(1, 0)
    ik.setOutputState(2, 0)
    ik.setOutputState(3, 0)

def cambiarEstadoPlaca(estado):
    """Método para cambiar el estado del sistema."""
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
        placa.set_estado_alerta('N')
    elif estado == 'M':
        if estadoActual == 'I' or estadoActual == 'C':
            __placa=iniciarPlaca()
            iniciarHiloLecturas()
            iniciarHiloEstadoAlertaSistema()
            iniciarHiloProcesarEstadoAlertaSistema()
    elif estado == 'A':
        if estadoActual == 'I' or estadoActual == 'C':
            __placa=iniciarPlaca()
            iniciarHiloLecturas()
            iniciarHiloEstadoAlertaSistema()
            iniciarHiloProcesarEstadoAlertaSistema()
        iniciarHiloNiveles()
    return None

def obtenerIkPadre (dispositivo):
    """
    @rtype: InterfaceKit
    @return: Devuelve el interface kit que controla al dispositivo pasado como parámetro"""
    padre= dispositivo.get_padre()
    if padre == None:
        return __placa.get_ik()
    else:
        return padre.get_ik()
    
    
    

def lecturaSensor(sensor):
    """Método que permite obtener una lectura de un sensor conectado a un puerto analógico ó digital,
    recibe como parámetro el sensor del que se pretende obtener la lectura.
    @rtype: float
    @return: Devuelve la lectura convertida a su valor final luego de aplicar la fórmula de conversión propia del sensor, ó -999 si hubo algún error"""
    ik= obtenerIkPadre (sensor)
    tipoPuerto= sensor.get_tipo_puerto()
    if tipoPuerto.get_nombre() == "analogico":
        try: 
            l=ik.getSensorValue(sensor.get_numero_puerto())
            if l < 10:
                temp=-999
                if sensor.get_estado_alerta() == 'N':
                    idTipoLog= TiposLogs.noSeEncuentraSensor
                    idMensaje= Mensajes.noSeEncuentraSensor
                    generarLogEvento(idTipoLog, idMensaje, sensor)
                    sensor.set_estado_alerta('S')
                    mbd= ManejadorBD()
                    con= mbd.getConexion()
                    mbd.cambiarEstadoAlerta(con, sensor.get_id_dispositivo(), 'S')
                    con.close()
            else:
                temp= eval(sensor.get_formula_conversion())
        except:
            
            temp= -999
    elif tipoPuerto.get_nombre() == "e-digital":
        try: 
            temp= ik.getInputState(sensor.get_numero_puerto())
        except:
            temp= -999
    return temp

def encenderActuador(actuador):
    """Método para encender un actuador perteneciente a un grupo de actuadores.
    @param actuador: Actuador que se desea encender
    @rtype: Char(1)
    @return: Devuelve el estado el que quedó el actuador ó 'F' si hubo algún error."""
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
        except:
            estado= 'F'
    return estado

def apagarActuador(actuador):
    """Método para apagar un actuador perteneciente a un grupo de actuadores.
    @param actuador: Actuador que se desea apagar
    @rtype: Char(1)
    @return: Devuelve el estado el que quedó el actuador ó 'F' si hubo algún error."""
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
        except:
            estado= 'F'
    return estado

def encenderGrupoActuadores(grupo):
    """Método para encender un grupo de actuadores.
    @param grupo: GrupoActuador que se desea encender
    @rtype: ResultadoAccion
    @return: Devuelve el ResultadoAccion obtenido al intentar encender el grupo de actuadores"""
    listaAcciones= list()
    listaActuadores= grupo.get_lista_actuadores()
    for actuador in listaActuadores:
        if actuador.get_estado_actuador() == 'A':
            estadoActuador=encenderActuador(actuador)
            if estadoActuador == 'F':
                print('ERROR ENCENDIDO ACTUADOR')
                if actuador.get_estado_alerta() == 'N':
                    idTipoLog= TiposLogs.errorEncendidoActuador
                    idMensaje= Mensajes.encendidoActuadorError   
                    generarLogEvento(idTipoLog, idMensaje, actuador)
                    actuador.set_estado_alerta('S')
                    mbd= ManejadorBD()
                    con= mbd.getConexion()
                    mbd.cambiarEstadoAlerta(con, actuador.get_id_dispositivo(), 'S')
                    con.close()
            else:
                mbd= ManejadorBD()
                con= mbd.getConexion()
                idActuador= actuador.get_id_dispositivo()
                mbd.insertarAccionActuador(con, idActuador, estadoActuador)
                con.commit()
                if actuador.get_estado_alerta() == 'S':
                    actuador.set_estado_alerta('N')
                    mbd= ManejadorBD()
                    con= mbd.getConexion()
                    mbd.cambiarEstadoAlerta(con, actuador.get_id_dispositivo(), 'N')
                    idTipoLog= TiposLogs.actuadorRecuperado
                    idMensaje= Mensajes.dispositivoRecuperado 
                    generarLogEvento(idTipoLog, idMensaje, actuador)
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
    """Método para apagar un grupo de actuadores.
    @param grupo: GrupoActuador que se desea apagar
    @rtype: ResultadoAccion
    @return: Devuelve el ResultadoAccion obtenido al intentar apagar el grupo de actuadores"""
    listaAcciones= list()
    listaActuadores= grupo.get_lista_actuadores()
    for actuador in listaActuadores:
        if actuador.get_estado_actuador() == 'E':
            estadoActuador=apagarActuador(actuador)
            if estadoActuador == 'F':
                print('ERROR APAGADO ACTUADOR')
                if actuador.get_estado_alerta() == 'N':
                    idTipoLog= TiposLogs.errorApagadoActuador
                    idMensaje= Mensajes.apagadoActuadorError  
                    generarLogEvento(idTipoLog, idMensaje, actuador)
                    actuador.set_estado_alerta('S')
                    mbd= ManejadorBD()
                    con= mbd.getConexion()
                    mbd.cambiarEstadoAlerta(con, actuador.get_id_dispositivo(), 'S')
                    con.close()
            else:
                mbd= ManejadorBD()
                con= mbd.getConexion()
                idActuador= actuador.get_id_dispositivo()
                mbd.insertarAccionActuador(con, idActuador, estadoActuador)
                con.commit()
                if actuador.get_estado_alerta() == 'S':
                    actuador.set_estado_alerta('N')
                    mbd= ManejadorBD()
                    con= mbd.getConexion()
                    mbd.cambiarEstadoAlerta(con, actuador.get_id_dispositivo(), 'N')
                    idTipoLog= TiposLogs.actuadorRecuperado
                    idMensaje= Mensajes.dispositivoRecuperado 
                    generarLogEvento(idTipoLog, idMensaje, actuador)
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
    """Método para crear y persisitir un dispositivo Sensor en el sistema.
    @rtype: int
    @return: Devuelve el identificador del dispositivo creado."""
    mbd= ManejadorBD()
    con= mbd.getConexion()
    idDispositivo=mbd.insertarDispositivo(con, nombre, modelo, nroPuerto)
    con.commit()
    mbd.insertarSensor(con, idDispositivo, formulaConversion, idTipoPuerto, idPlacaPadre, idFactor)
    con.commit()
    return idDispositivo

def crearActuador (nombre, modelo, nroPuerto, idTipoPuerto, idTipoActuador, idPlacaPadre, idGrupoActuadores):
    """Método para crear y persisitir un dispositivo Actuador en el sistema.
    @rtype: int
    @return: Devuelve el identificador del dispositivo creado."""
    mbd= ManejadorBD()
    con= mbd.getConexion()
    idDispositivo=mbd.insertarDispositivo(con, nombre, modelo, nroPuerto)
    con.commit()
    mbd.insertarActuador(con, idDispositivo, idTipoPuerto, idTipoActuador, idPlacaPadre, idGrupoActuadores)
    con.commit()
    return idDispositivo

def crearActuadorAvance (nombre, modelo, nroPuerto, posicion, idTipoPuerto, idTipoActuador, idPlacaPadre, nroPuertoRetroceso, tipoPuertoRetroceso, tiempoEntrePosiciones, idGrupoActuadores):
    """Método para crear y persisitir un dispositivo ActuadorAvance en el sistema.
    @rtype: int
    @return: Devuelve el identificador del dispositivo creado."""
    mbd= ManejadorBD()
    con= mbd.getConexion()
    idDispositivo=mbd.insertarDispositivo(con, nombre, modelo, nroPuerto)
    con.commit()
    mbd.insertarActuadorAvance(con, idDispositivo, posicion, idTipoPuerto, idTipoActuador, idPlacaPadre, nroPuertoRetroceso, tipoPuertoRetroceso, tiempoEntrePosiciones, idGrupoActuadores)
    con.commit()
    return idDispositivo

def crearPlacaAuxiliar (nombre, modelo, nroPuerto, nroSerie, idTipoPlaca, idPlacaPadre):
    """Método para crear y persisitir un dispositivo PlacaAuxiliar en el sistema.
    @rtype: int
    @return: Devuelve el identificador del dispositivo creado."""
    mbd= ManejadorBD()
    con= mbd.getConexion()
    idDispositivo=mbd.insertarDispositivo(con, nombre, modelo, nroPuerto)
    con.commit()
    mbd.insertarPlacaAuxiliar(con, idDispositivo, nroSerie, idTipoPlaca, idPlacaPadre)
    con.commit()
    return idDispositivo

def crearTipoPlaca (nombre):
    """Método para crear y persisitir un TipoPlaca en el sistema.
    @rtype: int
    @return: Devuelve el identificador del TipoPlaca creado."""
    mbd= ManejadorBD()
    con= mbd.getConexion()
    idTipoPlaca=mbd.insertarTipoPlaca(con, nombre)
    con.commit()
    return idTipoPlaca

def crearTipoActuador (nombre):
    """Método para crear y persisitir un TipoActuador en el sistema.
    @rtype: int
    @return: Devuelve el identificador del TipoActuador creado."""
    mbd= ManejadorBD()
    con= mbd.getConexion()
    idTipoActuador=mbd.insertarTipoActuador(con, nombre)
    con.commit()
    return idTipoActuador

def crearFactor(nombre, unidad, valorMin, valorMax, umbral):
    """Método para crear y persisitir un Factor en el sistema.
    @rtype: int
    @return: Devuelve el identificador del Factor creado."""
    mbd= ManejadorBD()
    con= mbd.getConexion()
    idFactor=mbd.insertarFactor(con, nombre, unidad, valorMin, valorMax, umbral)
    con.commit()
    con.close()
    return idFactor

def crearDestinatario(nombre, celular, mail, horaMin, horaMax):
    """Método para crear y persisitir un Destinatario en el sistema.
    @rtype: int
    @return: Devuelve el identificador del Destinatario creado."""
    mbd= ManejadorBD()
    con= mbd.getConexion()
    idDestinatario=mbd.insertarDestinatario(con, nombre, celular, mail, horaMin, horaMax)
    con.commit()
    con.close()
    return idDestinatario

def actualizarDestinatario(nombre, celular, mail, horaMin, horaMax, idDestinatario):
    """Método para actualizar los datos de un destinatario.
    @rtype: String
    @rtype: String
    @rtype: String
    @rtype: int
    @rtype: int
    @rtype: int
    @return: None"""
    mbd= ManejadorBD()
    con= mbd.getConexion()
    mbd.actualizarDestinatario(con, idDestinatario, nombre, celular, mail, horaMin, horaMax)
    con.close()
    return None

def actualizarSensor(idDispositivo, nombre, modelo, nroPuerto, formulaConversion, idTipoPuerto, idPlacaPadre, idFactor):
    """Método para actualizar los datos de un destinatario.
    @rtype: int
    @rtype: String
    @rtype: int
    @rtype: String
    @rtype: int
    @rtype: int
    @rtype: int
    @return: None"""
    mbd= ManejadorBD()
    con= mbd.getConexion()
    mbd.actualizarDispositivo(con, idDispositivo, nombre, modelo, nroPuerto)
    mbd.actualizarSensor(con, idDispositivo, formulaConversion, idTipoPuerto, idPlacaPadre, idFactor)
    con.close()
    return None

def actualizarPlacaAuxiliar(idDispositivo, nombre, modelo, nroSerie, idTipoPlaca, idPlacaPadre):
    """Método para actualizar los datos de un destinatario.
    @rtype: int
    @rtype: String
    @rtype: String
    @rtype: String
    @rtype: int
    @rtype: int
    @return: None"""
    mbd= ManejadorBD()
    con= mbd.getConexion()
    mbd.actualizarDispositivo(con, idDispositivo, nombre, modelo, None)
    mbd.actualizarPlacaAuxiliar(con, idDispositivo, nroSerie, idTipoPlaca, idPlacaPadre)
    con.close()
    return None

def actualizarPlaca(periodicidadLecturas, periodicidadNiveles):
    """Método para actualizar los datos de un destinatario.
    @rtype: int
    @rtype: int
    @return: None"""
    mbd= ManejadorBD()
    con= mbd.getConexion()
    mbd.actualizarPlaca(con, periodicidadLecturas, periodicidadNiveles)
    con.close()
    return None

def actualizarFactor(idFactor, nombre, unidad, valorMin, valorMax, umbral):
    """Método para actualizar los datos de un destinatario.
    @rtype: String
    @rtype: String
    @rtype: int
    @rtype: int
    @rtype: int
    @return: None"""
    mbd= ManejadorBD()
    con= mbd.getConexion()
    mbd.actualizarFactor(con, idFactor, nombre, unidad, valorMin, valorMax, umbral)
    con.close()
    return None

def actualizarActuador(idDispositivo, nombre, modelo, nroPuerto, idTipoPuerto, idTipoActuador, idPlacaPadre, idGrupoActuadores):
    """Método para actualizar los datos de un destinatario.
    @rtype: int
    @rtype: String
    @rtype: String
    @rtype: int
    @rtype: int
    @rtype: int
    @rtype: int
    @rtype: int
    @rtype: int
    @return: None"""
    mbd= ManejadorBD()
    con= mbd.getConexion()
    mbd.actualizarDispositivo(con, idDispositivo, nombre, modelo, nroPuerto)
    mbd.actualizarActuador(con, idDispositivo, idTipoPuerto, idTipoActuador, idPlacaPadre, idGrupoActuadores)
    con.close()
    return None

def actualizarActuadorAvance(idDispositivo, nombre, modelo, nroPuerto, posicion, idTipoPuerto, idTipoActuador, idPlacaPadre, nroPuertoRetroceso, tiempoEntrePosiciones, idGrupoActuadores):
    """Método para actualizar los datos de un destinatario.
    @rtype: int
    @rtype: String
    @rtype: String
    @rtype: int
    @rtype: Char(1)
    @rtype: int
    @rtype: int
    @rtype: int
    @rtype: int
    @rtype: int
    @rtype: int
    @return: None"""
    mbd= ManejadorBD()
    con= mbd.getConexion()
    mbd.actualizarDispositivo(con, idDispositivo, nombre, modelo, nroPuerto)
    mbd.actualizarActuadorAvance(con, idDispositivo, posicion, idTipoPuerto, idTipoActuador, idPlacaPadre, nroPuertoRetroceso, tiempoEntrePosiciones, idGrupoActuadores)
    con.close()
    return None

def actualizarGrupoActuadores(nombre, deAvance, idGrupoActuadores):
    """Método para actualizar los datos de un destinatario.
    @rtype: String
    @rtype: String
    @rtype: int
    @return: None"""
    mbd= ManejadorBD()
    con= mbd.getConexion()
    mbd.actualizarGrupoActuadores(con, idGrupoActuadores, nombre, deAvance)
    con.close()
    return None

def actualizarTipoActuador(nombre, idTipoActuador):
    """Método para actualizar los datos de un tipo de actuador.
    @rtype: String
    @rtype: int
    @return: None"""
    mbd= ManejadorBD()
    con= mbd.getConexion()
    mbd.actualizarTipoActuador(con, idTipoActuador, nombre)
    con.close()
    return None

def actualizarTipoPlaca(nombre, idTipoPlaca):
    """Método para actualizar los datos de un tipo de placa auxiliar.
    @rtype: String
    @rtype: int
    @return: None"""
    mbd= ManejadorBD()
    con= mbd.getConexion()
    mbd.actualizarTipoPlaca(con, idTipoPlaca, nombre)
    con.close()
    return None

def actualizarTipoLogEvento(enviarMail, enviarSMS, idTipoLogEvento):
    """Método para actualizar los datos de un tipo de log de evento.
    @rtype: String
    @rtype: String
    @rtype: int
    @return: None"""
    mbd= ManejadorBD()
    con= mbd.getConexion()
    mbd.actualizarTipoLogEvento(con, idTipoLogEvento, enviarMail, enviarSMS)
    con.close()
    return None

def eliminarPerfilActivacion(idNivelSeveridad):
    """Método para eliminar el perfil de activación perteneciente a un nivel de severidad.
    @rtype: int
    @return: None"""
    mbd= ManejadorBD()
    con= mbd.getConexion()
    mbd.eliminarPerfilActivacion(con, idNivelSeveridad)
    con.close()
    return None

def asociarDestinatarioTipoLogEvento(idTipoLogEvento, idDestinatario):
    """Método para asociar un destinatario existente a un tipo de log de eventos.
    @rtype: int
    @rtype: int
    @return: None"""
    mbd= ManejadorBD()
    con= mbd.getConexion()
    mbd.insertarDestinatarioTipoLog(con, idTipoLogEvento, idDestinatario)
    con.close()
    return None

def desasociarDestinatarioTipoLogEvento(idTipoLogEvento, idDestinatario):
    """Método para desasociar un destinatario existente a un tipo de log de eventos.
    @rtype: int
    @rtype: int
    @return: None"""
    mbd= ManejadorBD()
    con= mbd.getConexion()
    mbd.eliminarDestinatarioTipoLog(con, idTipoLogEvento, idDestinatario)
    con.close()
    return None

def eliminarDestinatario(idDestinatario):
    """Método para desasociar un destinatario existente a un tipo de log de eventos.
    @rtype: int
    @rtype: int
    @return: None"""
    mbd= ManejadorBD()
    con= mbd.getConexion()
    mbd.eliminarDestinatariosTipoLogs(con, idDestinatario)
    mbd.eliminarDestinatario(con, idDestinatario)
    con.close()
    return None

def crearGrupoActuadores(nombre, deAvance):
    """Método para crear y persisitir un GrupoActuador en el sistema.
    @rtype: int
    @return: Devuelve el identificador del GrupoActuador creado."""
    mbd= ManejadorBD()
    con= mbd.getConexion()
    idGrupo=mbd.insertarGrupoActuadores(con, nombre, deAvance)
    con.commit()
    con.close()
    return idGrupo

def crearNivelSeveridad (nombre, idFactor, prioridad, rangoMinimo, rangoMaximo):
    """Método para crear y persisitir un NivelSeveridad en el sistema.
    @rtype: int
    @return: Devuelve el identificador del NivelSeveridad creado."""
    mbd= ManejadorBD()
    con= mbd.getConexion()
    idNivel=mbd.insertarNivelSeveridad(con, nombre, idFactor, prioridad, rangoMinimo, rangoMaximo)
    con.commit()
    con.close()
    return idNivel

def actualizarNivelSeveridad (nombre, idFactor, prioridad, rangoMinimo, rangoMaximo, idNivelSeveridad):
    """Método para actualizar un NivelSeveridad en el sistema.
    @rtype: String
    @rtype: int
    @rtype: int
    @rtype: int
    @rtype: int
    @rtype: int
    @return: Devuelve el identificador del NivelSeveridad creado."""
    mbd= ManejadorBD()
    con= mbd.getConexion()
    mbd.actualizarNivelSeveridad(con, idNivelSeveridad, nombre, idFactor, prioridad, rangoMinimo, rangoMaximo)
    con.commit()
    con.close()
    return None

def asociarFactorSensor (idFactor, idDispositivo):
    """Método para asociar un sensor a un factor"""
    mbd= ManejadorBD()
    con= mbd.getConexion()
    mbd.asignarFactorSensor(con, idFactor, idDispositivo)
    con.commit()
    con.close()
    return None

def asociarGrupoActuadoresActuador (idGrupoActuadores, idDispositivo):
    """Método para asociar un sensor a un factor"""
    mbd= ManejadorBD()
    con= mbd.getConexion()
    mbd.asignarGrupoActuadoresActuador(con, idGrupoActuadores, idDispositivo)
    con.commit()
    con.close()
    return None

def asociarGrupoActuadoresActuadorAvance (idGrupoActuadores, idDispositivo):
    """Método para asociar un sensor a un factor"""
    mbd= ManejadorBD()
    con= mbd.getConexion()
    mbd.asignarGrupoActuadoresActuadorAvance(con, idGrupoActuadores, idDispositivo)
    con.commit()
    con.close()
    return None

def agregarFilaPerfilActivacion (idPerfilActivacion, idGrupoActuadores, estado):
    """Método para crear y persisitir una nueva fila perteneciente a un PerfilActivacion en el sistema."""
    mbd= ManejadorBD()
    con= mbd.getConexion()
    mbd.insertarFilaPerfilActivacion(con, idPerfilActivacion, idGrupoActuadores, estado)
    con.commit()
    con.close()
    return None

def agregarPosicionActuadorAvance (idActuadorAvance, numeroPosicion, descripcion, valor):
    """Método para crear y persisitir una Posicion perteneciente a un ActuadorAvance."""
    mbd= ManejadorBD()
    con= mbd.getConexion()
    mbd.insertarPosicionActuadorAvance(con, idActuadorAvance, numeroPosicion, descripcion, valor)
    con.commit()
    con.close()
    return None

def agregarSensorPosicionActuadorAvance (idSensor, idActuadorAvance, numeroPosicion):
    """Método para crear y persisitir un Sensor asociado a una Posicion perteneciente a un ActuadorAvance."""
    mbd= ManejadorBD()
    con= mbd.getConexion()
    mbd.insertarSensorPosicionActuadorAvance(con, idSensor, idActuadorAvance, numeroPosicion)
    con.commit()
    con.close()
    return None

def analizarLecturas(listaLecturas, factor):
    """Método para procesar una lista de lecturas de un factor pasado como parámetro. Realiza la selección de lecturas válidas y determina si alguna de estas está fuera de rango
    @rtype: float
    @return: Devuelve el la lectura promedio de las lecturas válidas, este luego es utilizado como la lectura del factor.
    """
    lecturasOk= list()
    listaValores= list()
    for tupla in listaLecturas:
        listaValores.append(tupla[0])
    if len(listaLecturas) > 1:
        for tuplaLectura in listaLecturas:
            lectura= tuplaLectura[0]
            if lectura < factor.get_valor_min() or lectura > factor.get_valor_max() :
                print 'LECTURA FUERA DE RANGO'
                sensor= tuplaLectura[1]
                if sensor.get_estado_alerta() == 'N':
                    idTipoLog= TiposLogs.lecturaFueraRango
                    idMensaje= Mensajes.lecturaFueraRango
                    generarLogEvento(idTipoLog, idMensaje, sensor)
                    sensor.set_estado_alerta('S')
                    mbd= ManejadorBD()
                    con= mbd.getConexion()
                    mbd.cambiarEstadoAlerta(con, sensor.get_id_dispositivo(), 'S')
                    con.close()
            else:
                promedioResto= (sum(listaValores) - lectura) / (len(listaValores) - 1)
                diferencia= lectura - promedioResto
                if diferencia < 0:
                    diferencia= diferencia * -1
                if diferencia < factor.get_umbral():
                    lecturasOk.append(lectura)
                    sensor= tuplaLectura[1]
                    if sensor.get_estado_alerta() == 'S':
                        sensor.set_estado_alerta('N')
                        mbd= ManejadorBD()
                        con= mbd.getConexion()
                        mbd.cambiarEstadoAlerta(con, sensor.get_id_dispositivo(), 'N')
                        idTipoLog= TiposLogs.sensorRecuperado
                        idMensaje= Mensajes.dispositivoRecuperado 
                        generarLogEvento(idTipoLog, idMensaje, sensor)
                        con.close()
                else:
                    print 'LECTURA FUERA DE UMBRAL PERMITIDO'
                    sensor= tuplaLectura[1]
                    if sensor.get_estado_alerta() == 'N':
                        idTipoLog= TiposLogs.lecturaFueraUmbral
                        idMensaje= Mensajes.lecturaFueraUmbral
                        generarLogEvento(idTipoLog, idMensaje, sensor)
                        sensor.set_estado_alerta('S')
                        mbd= ManejadorBD()
                        con= mbd.getConexion()
                        mbd.cambiarEstadoAlerta(con, sensor.get_id_dispositivo(), 'S')
                        con.close()
    else:
        lectura= listaLecturas[0][0]
        if lectura < factor.get_valor_min() or lectura > factor.get_valor_max() :
            print 'LECTURA FUERA DE RANGO'
            sensor= listaLecturas[0][1]
            if sensor.get_estado_alerta() == 'N':
                idTipoLog= TiposLogs.lecturaFueraRango
                idMensaje= Mensajes.lecturaFueraRango
                generarLogEvento(idTipoLog, idMensaje, sensor)
                sensor.set_estado_alerta('S')
                mbd= ManejadorBD()
                con= mbd.getConexion()
                mbd.cambiarEstadoAlerta(con, sensor.get_id_dispositivo(), 'S')
                con.close()
        else:
            lecturasOk.append(lectura)
            sensor= listaLecturas[0][1]
            if sensor.get_estado_alerta() == 'S':
                idTipoLog= TiposLogs.sensorRecuperado
                idMensaje= Mensajes.dispositivoRecuperado
                generarLogEvento(idTipoLog, idMensaje, sensor)
                sensor.set_estado_alerta('N')
                mbd= ManejadorBD()
                con= mbd.getConexion()
                mbd.cambiarEstadoAlerta(con, sensor.get_id_dispositivo(), 'N')
                con.close()
    if len(lecturasOk) == 0:
        print ('NINGUNA LECTURA VALIDA')
        return 'E'
    else: 
        resultado= sum(lecturasOk) / len(lecturasOk) 
        return resultado

def procesarLecturaFactor(factor): 
    """Método que posibilita tomar lecturas de todos los sensores pertenecientes a un factor y devuelve un promedio de dichas lecturas como una única lectura final del factor.
    @param factor: Factor sobre el que se desea procesar sus lecturas
    @rtype: float
    @return: Valor de lectura final del Factor."""
    listaSensores= factor.get_lista_sensores()
    listaLecturas= list()
    for sensor in listaSensores:
        lectura=(lecturaSensor(sensor), sensor)
        mbd= ManejadorBD()
        con= mbd.getConexion()
        mbd.insertarLecturaSensor(con, sensor.get_id_dispositivo(), lectura[0])
        con.commit()
        con.close()
        if lectura[0] <> -999:
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

def eliminarFactor(idFactor):
    """Método para realizar el eliminado lógico de un factor del sistema."""
    mbd= ManejadorBD()
    con= mbd.getConexion()
    mbd.eliminadoLogicoFactor(con, idFactor)
    con.commit()
    con.close()
    return None

def eliminarDispositivo(idDispositivo):
    """Método para realizar el eliminado lógico de un dispositivo del sistema."""
    mbd= ManejadorBD()
    con= mbd.getConexion()
    mbd.eliminadoLogicoDispositivo(con, idDispositivo)
    con.commit()
    con.close()
    return None

def eliminarGrupoActuadores(idGrupoActuadores):
    """Método para realizar el eliminado lógico de un grupo de actuadores del sistema."""
    mbd= ManejadorBD()
    con= mbd.getConexion()
    mbd.eliminadoLogicoGrupoActuadores(con, idGrupoActuadores)
    con.commit()
    con.close()
    return None

def eliminarNivelSeveridad(idNivelSeveridad):
    """Método para realizar el eliminado lógico de un nivel de severidad del sistema."""
    mbd= ManejadorBD()
    con= mbd.getConexion()
    mbd.eliminadoLogicoNivelSeveridad(con, idNivelSeveridad)
    con.commit()
    con.close()
    return None

def eliminarFilaPerfilActivacion(idPerfil, idGrupoActuadores):
    """Método para realizar el eliminado lógico de una fila perteneciente a un perfil de activación del sistema."""
    mbd= ManejadorBD()
    con= mbd.getConexion()
    mbd.eliminadoLogicoFilaPerfilActivacion(con, idPerfil, idGrupoActuadores)
    con.commit()
    con.close()
    return None

def generarLogEvento(idTipoLog, idMensaje, dispositivo):
    """Método para generar y persistir un LogEvento, e invocar a los mecanismos de notificación asociados al TipoLog al que pertenece el LogEvento generado.
    @param idTipoLog: Identificador del TipoLog al que pertenece el LogEvento
    @param idMensaje: Identificador del mensaje asociado al LogEvento
    @param dispositivo: Dispositivo que genera el LogEvento."""
    mbd= ManejadorBD()
    con= mbd.getConexion()
    tipoLogEvento=mbd.obtenerTipoLogEvento(con, idTipoLog)
    mensaje=mbd.obtenerMensaje(con, idMensaje)
    fecha= datetime.now()
    if dispositivo <> 0:
        idLogEvento=mbd.insertarLogEvento(con, idTipoLog, dispositivo.get_id_dispositivo(), idMensaje, fecha)
    else:
        idLogEvento=mbd.insertarLogEvento(con, idTipoLog, 0, idMensaje, fecha)
    logEvento= LogEvento(idLogEvento, tipoLogEvento, dispositivo, mensaje, fecha)
    
    mbd= ManejadorBD()
    con= mbd.getConexion()
    datosAC= mbd.obtenerHostPuertoWS_Centralizadora(con)
    
    sendLec= SendLectura(datosAC[0], datosAC[1])
    ok= sendLec.enviarLogEvento(__placa.get_nro_serie(), logEvento)
    if (ok):
        mbd.marcarLogEventoInformada(con, idLogEvento)
        
    if (tipoLogEvento.get_enviar_sms() == 'S'):
        hostPuerto= mbd.obtenerHostPuertoWS_SMS(con)
        sms= SMS(hostPuerto[0], hostPuerto[1])
        if sms.enviarSMS(logEvento) == 'F':
            idTipoLog= TiposLogs.errorSMS
            idMensaje= Mensajes.falloSMS
            generarLogEvento(idTipoLog, idMensaje, 0)
    if (tipoLogEvento.get_enviar_mail() == 'S'):
        print('ENVIAR MAIL')
        """LLAMAR A METODO DE ENVIO DE MAIL POR WS"""
    con.close()

def cambiarPosicionActuadorAvance(actuadorAvance, nroDestino):
    """Método para cambiar de posicion un actuador de avance.
    @param actuadorAvance: Actuador de avance al que se pretende cambiar de posición
    @param nroDestino: Número de posición al que se pretende cambiar el actuador de avance
    @rtype: Char(1)
    @return: Devuelve la posición en la que quedó el actuador de avance, ó 'F' en caso de que haya ocurrido algún error."""
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
            if ik <> None and actuadorAvance.get_estado_alerta() <> 'S':
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
                    if actuadorAvance.get_estado_alerta() == 'N':
                        actuadorAvance.set_estado_alerta('S')
                        mbd= ManejadorBD()
                        con= mbd.getConexion()
                        mbd.cambiarEstadoAlerta(con, actuadorAvance.get_id_dispositivo(), 'S')
                        con.close()
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
                    if actuadorAvance.get_estado_alerta() == 'S':
                        actuadorAvance.set_estado_alerta('N')
                        mbd= ManejadorBD()
                        con= mbd.getConexion()
                        mbd.cambiarEstadoAlerta(con, actuadorAvance.get_id_dispositivo(), 'N')
                        idTipoLog= TiposLogs.actuadorRecuperado
                        idMensaje= Mensajes.dispositivoRecuperado
                        generarLogEvento(idTipoLog, idMensaje, actuadorAvance)
                    if actuadorAvance.get_padre().get_estado_alerta() == 'S':
                        actuadorAvance.get_padre().set_estado_alerta('N')
                        mbd= ManejadorBD()
                        con= mbd.getConexion()
                        mbd.cambiarEstadoAlerta(con, actuadorAvance.get_padre().get_id_dispositivo(), 'N')
                        idTipoLog= TiposLogs.placaAuxiliarRecuperada
                        idMensaje= Mensajes.dispositivoRecuperado
                        generarLogEvento(idTipoLog, idMensaje, actuadorAvance.get_padre())
                    con.close()
                    return nroDestino
            else:
                if actuadorAvance.get_padre().get_estado_alerta() == 'N':
                    actuadorAvance.get_padre().set_estado_alerta('S')
                    mbd= ManejadorBD()
                    con= mbd.getConexion()
                    mbd.cambiarEstadoAlerta(con, actuadorAvance.get_padre().get_id_dispositivo(), 'S')
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
            if ik <> None and actuadorAvance.get_estado_alerta() <> 'S':
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
                    if actuadorAvance.get_estado_alerta() == 'N':
                        actuadorAvance.set_estado_alerta('S')
                        mbd= ManejadorBD()
                        con= mbd.getConexion()
                        mbd.cambiarEstadoAlerta(con, actuadorAvance.get_id_dispositivo(), 'S')
                        con.close()
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
                    if actuadorAvance.get_estado_alerta() == 'S':
                        actuadorAvance.set_estado_alerta('N')
                        mbd= ManejadorBD()
                        con= mbd.getConexion()
                        mbd.cambiarEstadoAlerta(con, actuadorAvance.get_id_dispositivo(), 'N')
                        idTipoLog= TiposLogs.actuadorRecuperado
                        idMensaje= Mensajes.dispositivoRecuperado
                        generarLogEvento(idTipoLog, idMensaje, actuadorAvance)
                    if actuadorAvance.get_padre().get_estado_alerta() == 'S':
                        actuadorAvance.get_padre().set_estado_alerta('N')
                        mbd= ManejadorBD()
                        con= mbd.getConexion()
                        mbd.cambiarEstadoAlerta(con, actuadorAvance.get_padre().get_id_dispositivo(), 'N')
                        idTipoLog= TiposLogs.placaAuxiliarRecuperada
                        idMensaje= Mensajes.dispositivoRecuperado
                        generarLogEvento(idTipoLog, idMensaje, actuadorAvance.get_padre())
                    con.close()
                    return nroDestino
            else:
                if actuadorAvance.get_padre().get_estado_alerta() == 'N':
                    actuadorAvance.get_padre().set_estado_alerta('S')
                    mbd= ManejadorBD()
                    con= mbd.getConexion()
                    mbd.cambiarEstadoAlerta(con, actuadorAvance.get_padre().get_id_dispositivo(), 'S')
                    idTipoLog= TiposLogs.noSePuedeInstanciarPadre
                    idMensaje= Mensajes.noSePuedeInstanciarPadre
                    generarLogEvento(idTipoLog, idMensaje, actuadorAvance.get_padre())
                return 'F'
        else:
            print ("El actuador de avance no tiene esa posicion")
            return 'F'
            
def cambiarPosicionGrupoActuadores(grupo, nroPosicion):
    """Método para cambiar de posicion un grupo de actuadores de avance.
    @param grupo: Grupo de actuadores de avance al que se pretende cambiar de posición
    @param nroDestino: Número de posición al que se pretende cambiar el actuador de avance
    @rtype: ResultadoAccion
    @return: Devuelve el ResultadoAccion generado al intentar cambiar de posición al grupo de actuadores de avance."""
    listaAcciones= list()
    listaActuadores= grupo.get_lista_actuadores()
    for actuadorAvance in listaActuadores:
        posicionActual= actuadorAvance.get_posicion()
        if posicionActual <> nroPosicion:
            estadoActuador=cambiarPosicionActuadorAvance(actuadorAvance, nroPosicion)
            if estadoActuador == 'F':
                print('ERROR CAMBIO POSICION ACTUADOR')
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
    """Método utilizado desde los hilos secundarios del sistema para obtener la instancia de la placa generada en el hilo principal."""
    return __placa

def convertirResultadoLectura(resultadoLectura):
    """Método para convertir un ResultadoLectura a un ResultadoLecturaWS.
    @param resultadoLectura: ResultadoLectura a convertir
    @rtype: ResultadoLecturaWS
    @return: Devuelve el ResultadoLectura convertido a ResultadoLecturaWS"""
    mensaje= resultadoLectura.get_mensaje()
    fecha= resultadoLectura.get_fecha()
    idFactor= resultadoLectura.get_id_factor()
    valor= resultadoLectura.get_valor()
    resultado= ResultadoLecturaWS(mensaje, fecha, idFactor, valor)
    return resultado

def convertirResultadoAccion(resultadoAccion):
    """Método para convertir un ResultadoAccion a un ResultadoAccionWS.
    @param resultadoLectura: ResultadoAccion a convertir
    @rtype: ResultadoAccionWS
    @return: Devuelve el ResultadoAccion convertido a ResultadoAccionWS"""
    mensaje= resultadoAccion.get_mensaje()
    fecha= resultadoAccion.get_fecha()
    idGrupoActuadores= resultadoAccion.get_id_grupo_actuadores()
    tipoAccion= resultadoAccion.get_tipo_accion()
    resultado= ResultadoAccionWS(mensaje, fecha, idGrupoActuadores, tipoAccion)
    return resultado

def reestablecerEstadoAlerta(idDispositivo):
    """Método para reestablecer del estado de alerta al Dispositivo que se corresponde con el identificador pasado como parámetro"""
    mbd= ManejadorBD()
    con= mbd.getConexion()
    mbd.cambiarEstadoAlerta(con, idDispositivo, 'N')
    con.commit()
    con.close()
    
def reestablecerActuadorAvance(idDispositivo, numeroPosicion):
    """Método para reestablecer del estado de alerta al ActuadorAvance que se corresponde con el identificador pasado como parámetro, y asignar su posición luego de reestablecido"""
    mbd= ManejadorBD()
    con= mbd.getConexion()
    mbd.recuperarActuadorAvance(con, idDispositivo, numeroPosicion)
    con.close()

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
    
    @soapmethod(Integer, Integer,_returns=Mensaje)
    def wsAsociarFactorSensor(self, idFactor, idDispositivo):
        asociarFactorSensor(idFactor, idDispositivo)
        idMensaje= Mensajes.asociarSensorFactorOk
        mbd= ManejadorBD()
        con= mbd.getConexion()
        mensaje=mbd.obtenerMensaje(con, idMensaje)
        con.close()
        return mensaje
    
    @soapmethod(Integer, Integer,_returns=Mensaje)
    def wsAsociarDestinatarioTipoLogEvento(self, idTipoLogEvento, idDestinatario):
        asociarDestinatarioTipoLogEvento(idTipoLogEvento, idDestinatario)
        idMensaje= Mensajes.destinatarioAsociadoTipoLogOk
        mbd= ManejadorBD()
        con= mbd.getConexion()
        mensaje=mbd.obtenerMensaje(con, idMensaje)
        con.close()
        return mensaje
    
    @soapmethod(Integer, Integer,_returns=Mensaje)
    def wsDesasociarDestinatarioTipoLogEvento(self, idTipoLogEvento, idDestinatario):
        desasociarDestinatarioTipoLogEvento(idTipoLogEvento, idDestinatario)
        idMensaje= Mensajes.destinatarioAsociadoTipoLogOk
        mbd= ManejadorBD()
        con= mbd.getConexion()
        mensaje=mbd.obtenerMensaje(con, idMensaje)
        con.close()
        return mensaje
    
    @soapmethod(Integer, _returns=Mensaje)
    def wsEliminarDestinatario(self, idDestinatario):
        eliminarDestinatario(idDestinatario)
        idMensaje= Mensajes.DestinatarioEliminadoOk
        mbd= ManejadorBD()
        con= mbd.getConexion()
        mensaje=mbd.obtenerMensaje(con, idMensaje)
        con.close()
        return mensaje
    
    @soapmethod(Integer, Integer,_returns=Mensaje)
    def wsAsociarActuadorGrupo(self, idGrupoActuadores, idDispositivo):
        asociarGrupoActuadoresActuador(idGrupoActuadores, idDispositivo)
        idMensaje= Mensajes.asociarSensorFactorOk
        mbd= ManejadorBD()
        con= mbd.getConexion()
        mensaje=mbd.obtenerMensaje(con, idMensaje)
        con.close()
        return mensaje
    
    @soapmethod(Integer, Integer,_returns=Mensaje)
    def wsAsociarActuadorAvanceGrupo(self, idGrupoActuadores, idDispositivo):
        asociarGrupoActuadoresActuadorAvance(idGrupoActuadores, idDispositivo)
        idMensaje= Mensajes.asociarSensorFactorOk
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
            idFactor= crearFactor(unicode(nombre, 'utf8'), unicode(unidad, 'utf8'), valorMin, valorMax, umbral)
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
    
    
    @soapmethod(String, String, String, Integer, Integer, _returns=ResultadoCreacionWS)
    def wsCrearDestinatario(self, nombre, celular, mail, horaMin, horaMax):
        placa= getPlaca()
        estadoSistema= placa.get_estado_sistema()
        if estadoSistema == 'C':
            idDestinatario= crearDestinatario(unicode(nombre, 'utf8'), unicode(celular, 'utf8'), unicode(mail, 'utf8'), horaMin, horaMax)
            idMensaje= Mensajes.destinatarioCreadoOk
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
        resultado= ResultadoCreacionWS(mensaje, idDestinatario)
        return resultado
    
    @soapmethod(String, String, String, Integer, Integer, Integer, _returns=Mensaje)
    def wsActualizarDestinatario(self, nombre, celular, mail, horaMin, horaMax, idDestinatario):
        placa= getPlaca()
        estadoSistema= placa.get_estado_sistema()
        if estadoSistema == 'C':
            actualizarDestinatario(unicode(nombre, 'utf8'), unicode(celular, 'utf8'), unicode(mail, 'utf8'), horaMin, horaMax, idDestinatario)
            idMensaje= Mensajes.destinatarioActualizadoOk
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
    
    @soapmethod(String, String, Integer, String, Integer, Integer, Integer, Integer, _returns=Mensaje)
    def wsActualizarSensor(self, nombre, modelo, nroPuerto, formulaConversion, idTipoPuerto, idPlacaPadre, idFactor, idDispositivo):
        placa= getPlaca()
        estadoSistema= placa.get_estado_sistema()
        if estadoSistema == 'C':
            actualizarSensor(idDispositivo, unicode(nombre, 'utf8'), unicode(modelo, 'utf8'), nroPuerto, unicode(formulaConversion, 'utf8'), idTipoPuerto, idPlacaPadre, idFactor)
            idMensaje= Mensajes.sensorActualizadoOk
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
    
    @soapmethod(String, String, String, Integer, Integer, Integer, _returns=Mensaje)
    def wsActualizarPlacaAuxiliar(self, nombre, modelo, nroSerie, idTipoPlaca, idPlacaPadre, idDispositivo):
        placa= getPlaca()
        estadoSistema= placa.get_estado_sistema()
        if estadoSistema == 'C':
            actualizarPlacaAuxiliar(idDispositivo, unicode(nombre, 'utf8'), unicode(modelo, 'utf8'), unicode(nroSerie, 'utf8'), idTipoPlaca, idPlacaPadre)
            idMensaje= Mensajes.PlacaAuxiliarActualizadaOk
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
    def wsActualizarPlaca(self, periodicidadLecturas, periodicidadNiveles):
        placa= getPlaca()
        estadoSistema= placa.get_estado_sistema()
        if estadoSistema == 'C':
            actualizarPlaca(periodicidadLecturas, periodicidadNiveles)
            idMensaje= Mensajes.PlacaControladoraActualizadaOk
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
    
    @soapmethod(String, String, Integer, Integer, Integer, Integer, _returns=Mensaje)
    def wsActualizarFactor(self, nombre, unidad, valorMin, valorMax, umbral, idFactor):
        placa= getPlaca()
        estadoSistema= placa.get_estado_sistema()
        if estadoSistema == 'C':
            actualizarFactor(idFactor, unicode(nombre, 'utf8'), unicode(unidad, 'utf8'), valorMin, valorMax, umbral)
            idMensaje= Mensajes.FactorActualizadoOk
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
    
    @soapmethod(String, Integer, Integer, Integer, Integer, Integer, _returns=Mensaje)
    def wsActualizarNivelSeveridad(self, nombre, idFactor, prioridad, rangoMinimo, rangoMaximo, idNivelSeveridad):
        placa= getPlaca()
        estadoSistema= placa.get_estado_sistema()
        if estadoSistema == 'C':
            actualizarNivelSeveridad(unicode(nombre, 'utf8'), idFactor, prioridad, rangoMinimo, rangoMaximo, idNivelSeveridad)
            idMensaje= Mensajes.NivelSeveridadActualizadoOk
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
    
    @soapmethod(String, String, Integer, Integer, Integer, Integer, Integer, Integer, _returns=Mensaje)
    def wsActualizarActuador(self, nombre, modelo, nroPuerto, idTipoPuerto, idTipoActuador, idPlacaPadre, idGrupoActuadores, idDispositivo):
        placa= getPlaca()
        estadoSistema= placa.get_estado_sistema()
        if estadoSistema == 'C':
            actualizarActuador(idDispositivo, unicode(nombre, 'utf8'), unicode(modelo, 'utf8'), nroPuerto, idTipoPuerto, idTipoActuador, idPlacaPadre, idGrupoActuadores)
            idMensaje= Mensajes.ActuadorActualizadoOk
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
    
    @soapmethod(String, String, Integer, Integer, Integer, Integer, Integer, Integer, Integer, Integer, Integer, _returns=Mensaje)
    def wsActualizarActuadorAvance(self, nombre, modelo, nroPuerto, posicion, idTipoPuerto, idTipoActuador, idPlacaPadre, nroPuertoRetroceso, tiempoEntrePosiciones, idGrupoActuadores, idDispositivo):
        placa= getPlaca()
        estadoSistema= placa.get_estado_sistema()
        if estadoSistema == 'C':
            actualizarActuadorAvance(idDispositivo, unicode(nombre, 'utf8'), unicode(modelo, 'utf8'), nroPuerto, posicion, idTipoPuerto, idTipoActuador, idPlacaPadre, nroPuertoRetroceso, tiempoEntrePosiciones, idGrupoActuadores)
            idMensaje= Mensajes.ActuadorAvanceActualizadoOk
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
    
    @soapmethod(String, String, Integer, _returns=Mensaje)
    def wsActualizarGrupoActuadores(self, nombre, deAvance, idGrupoActuadores):
        placa= getPlaca()
        estadoSistema= placa.get_estado_sistema()
        if estadoSistema == 'C':
            actualizarGrupoActuadores(unicode(nombre, 'utf8'), unicode(deAvance, 'utf8'), idGrupoActuadores) 
            idMensaje= Mensajes.GrupoActuadoresActualizadoOk
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
    
    @soapmethod(String, Integer, _returns=Mensaje)
    def wsActualizarTipoActuador(self, nombre, idTipoActuador):
        placa= getPlaca()
        estadoSistema= placa.get_estado_sistema()
        if estadoSistema == 'C':
            actualizarTipoActuador(unicode(nombre, 'utf8'), idTipoActuador) 
            idMensaje= Mensajes.TipoActuadorActualizadoOk
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
    
    @soapmethod(String, Integer, _returns=Mensaje)
    def wsActualizarTipoPlaca(self, nombre, idTipoPlaca):
        placa= getPlaca()
        estadoSistema= placa.get_estado_sistema()
        if estadoSistema == 'C':
            actualizarTipoPlaca(unicode(nombre, 'utf8'), idTipoPlaca) 
            idMensaje= Mensajes.TipoPlacaActualizadoOk
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
    
    @soapmethod(String, String, Integer, _returns=Mensaje)
    def wsActualizarTipoLogEvento(self, enviarMail, enviarSMS, idTipoLogEvento):
        placa= getPlaca()
        estadoSistema= placa.get_estado_sistema()
        if estadoSistema == 'C':
            actualizarTipoLogEvento(enviarMail, enviarSMS, idTipoLogEvento)
            idMensaje= Mensajes.TipoLogEventoActualizadoOk
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
    
    @soapmethod(String, String, _returns=ResultadoCreacionWS)
    def wsCrearGrupoActuadores(self, nombre, deAvance):
        placa= getPlaca()
        estadoSistema= placa.get_estado_sistema()
        if estadoSistema == 'C':
            idGrupo= crearGrupoActuadores(unicode(nombre, 'utf8'), deAvance)
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
            idSensor= crearSensor(unicode(nombre, 'utf8'), unicode(modelo, 'utf8'), nroPuerto, unicode(formulaConversion, 'utf8'), idTipoPuerto, idPlacaPadre, idFactor)
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
            idActuador= crearActuador(unicode(nombre, 'utf8'), unicode(modelo, 'utf8'), nroPuerto, idTipoPuerto, idTipoActuador, idPlacaPadre, idGrupoActuadores)
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
            idTipoPlaca= crearTipoPlaca(unicode(nombre, 'utf8'))
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
            idTipoActuador= crearTipoActuador(unicode(nombre, 'utf8'))
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
            idPlacaAuxiliar= crearPlacaAuxiliar(unicode(nombre, 'utf8'), unicode(modelo, 'utf8'), nroPuerto, unicode(nroSerie, 'utf8'), idTipoPlaca, idPlacaPadre)
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
            idNivel= crearNivelSeveridad(unicode(nombre, 'utf8'), idFactor, prioridad, rangoMinimo, rangoMaximo)
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
            idActuadorAvance= crearActuadorAvance(unicode(nombre, 'utf8'), unicode(modelo, 'utf8'), nroPuerto, posicion, idTipoPuerto, idTipoActuador, idPlacaPadre, nroPuertoRetroceso, tipoPuertoRetroceso, tiempoEntrePosiciones, idGrupoActuadores)
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
    def wsEliminarPerfilActivacion(self, idNivelSeveridad):
        placa= getPlaca()
        estadoSistema= placa.get_estado_sistema()
        if estadoSistema == 'C':
            eliminarPerfilActivacion(idNivelSeveridad)
            idMensaje= Mensajes.PerfilActivacionEliminadoOk
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
    
    @soapmethod(Integer, _returns=ResultadoDatosPlacaWS)
    def wsObtenerDatosPlaca(self, temp):
        datosPlaca=obtenerDatosPlaca()
        resultado= ResultadoDatosPlacaWS(datosPlaca.get_nro_serie_placa(), datosPlaca.get_estado_placa(), datosPlaca.get_host_ws_sms(), datosPlaca.get_puerto_ws_sms(), datosPlaca.get_host_ws_centralizadora(), datosPlaca.get_puerto_ws_centralizadora(), datosPlaca.get_periodicidad_lecturas(), datosPlaca.get_periodicidad_niveles(), datosPlaca.get_estado_alerta())
        return resultado
    
    @soapmethod(String, _returns=String)
    def wsObtenerEstadoAlertaPlaca(self, nroSerie):
        estadoAlerta=obtenerEstadoAlertaSistema()
        return estadoAlerta
    
    @soapmethod(Integer, _returns=String)
    def wsObtenerEstadoAlertaDispositivo(self, idDispositivo):
        estadoAlerta=obtenerEstadoAlertaDispostivo(idDispositivo)
        return estadoAlerta
    
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
    
    @soapmethod(Integer,  _returns=Mensaje)
    def wsReestablecerEstadoAlertaDispositivo(self, idDispositivo):
        placa= getPlaca()
        estadoSistema= placa.get_estado_sistema()
        if estadoSistema == 'C':
            reestablecerEstadoAlerta(idDispositivo)
            idMensaje= Mensajes.dispositivoRecuperado
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
    
    @soapmethod(Integer, Integer,  _returns=Mensaje)
    def wsReestablecerActuadorAvance(self, idDispositivo, numeroPosicion):
        placa= getPlaca()
        estadoSistema= placa.get_estado_sistema()
        if estadoSistema == 'C':
            reestablecerActuadorAvance(idDispositivo, numeroPosicion)
            idMensaje= Mensajes.dispositivoRecuperado
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
    """Método invocado automáticamente al ejecutar el módulo Main, que pone en funcionamiento el sistema."""
    __placa=iniciarPlaca()
    if __placa <> None:
        apagarTodo()
        iniciarHiloWS()
        estado= __placa.get_estado_sistema()
        if estado == 'M' or estado == 'A':
            iniciarHiloLecturas()
            iniciarHiloEstadoAlertaSistema()
            iniciarHiloProcesarEstadoAlertaSistema()
            iniciarHiloInformeLecturas()
            iniciarHiloInformeAcciones()
            iniciarHiloInformeLogEventos()
        if estado == 'A':
            iniciarHiloNiveles()
    else:
        print('Sistema finalizado...')
