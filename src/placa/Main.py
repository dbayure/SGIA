# -*- encoding: utf-8 -*-
"""
Módulo principal del sistema, es el encargado de iniciar la ejecución del mismo.
Debe instanciar la placa y el servidor de WS, además es encargado de comunicarse con la 
capa de persistencia para guardar y recuperar datos.
Tiene como atributos una instancia única de placa y una instancia única de ws.
"""
from src.bdd.ManejadorBD import ManejadorBD
from src.placa.Placa import Placa
from Phidgets.Devices.InterfaceKit import InterfaceKit
from Phidgets.PhidgetException import PhidgetException

ipWS= '192.168.0.103'
puertoWS= 5001
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
            while idSensor <>listaDispositivos[i].get_id_dispositivo() and i < len(listaDispositivos):
                i= i+1
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
            i=0
            while i < len(listaDispositivos) and (idActuador <>listaDispositivos[i].get_id_dispositivo()) :
                i= i+1
            if i < len(listaDispositivos):
                actuador= listaDispositivos[i]
                listaActuadores.append(actuador)
        grupo.set_lista_actuadores(listaActuadores)
    mbd.cerrarConexion()
    #aca la lista de grupos de actuadores ya está actualizada con la lista de actuadores de cada una 
    #Tengo todo lo necesario para instanciar el objeto Placa
    placa= Placa(nroSerie, estadoSistema, listaDispositivos, listaGrupoActuadores, listaFactores)     
    return placa

def instanciarIK (nroSerie):
    """
    Método utilizado para instanciar un objeto de tipo InterfaceKit de la API de Phidgets, que permite interactuar con 
    la placa controladora y sus puertos"""
    ik= InterfaceKit()
    ik.openRemoteIP(ipWS, puertoWS, nroSerie)
    return ik

def iniciarWS(): #DESPUES
    return None

def cambiarEstadoPlaca(estado):
    return None

def chequeoPlaca(): #DESPUES
    return None

def chequeoDispositivo(idDispositivo): #DESPUES
    return None

def chequeoDispositivos(): #DESPUES
    return None

def lecturaSensor(sensor, ik):
    """Método que permite obtener una lectura de un sensor conectado a un puerto analógico o digital,
    recibe como parámetros el sensor del que se pretende obtener la lectura y el interface kit que puede 
    interactuar con dicho sensor. Devuelve la lectura convertida a su valor final luego de aplicar la fórmula 
    propia del sensor"""
    tipoPuerto= sensor.get_tipo_puerto()
    if tipoPuerto.get_nombre() == "analogico":
        valor=ik.getSensorValue(sensor.get_numero_puerto())
        print ('Valor bruto: '+ str(valor))
        l=valor
        temp= eval(sensor.get_formula_conversion())
    elif tipoPuerto.get_nombre() == "e-digital":
        temp= ik.getInputState(sensor.get_numero_puerto())
    return temp

def encenderActuador(idDispositivo):
    return None

def apagarActuador(idDispositivo):
    return None

def encenderGrupoActuadores(idGrupoActuadores):
    return None

def apagarGrupoActuadores(idGrupoActuadores):
    return None

def cargarNivelPerfil(nivelSeveridad, perfilActivacion): #DESPUES
    return None

def eliminarNivelPerfil (idNivelSeveridad): #DESPUES
    return None

def cargarDispositivo (dispositivo): #DESPUES
    return None

def eliminarDispositivo (idDispositivo): #DESPUES
    return None

def iniciarComportamientoAutomatico(): #DESPUES
    return None

def detenerComportamientoAutomatico(control): #DESPUES
    return None

def iniciarChequeosAutomaticos(): #DESPUES
    return None

def procesarLecturaFactor(factor, ik): 
    """Método que posibilita tomar lecturas de todos los sensores pertenecientes a un factor y devuelve
    un promedio de dichas lecturas como una única lectura perteneciente al factor.
    Recibe como parámetros un factor y un interfaceKit que permite interactuar con cada sensor.
    Devuelve una lectura promedio en formato float"""
    listaSensores= factor.get_lista_sensores()
    print('Lecturas del factor: '+ factor.get_nombre())
    listaLecturas= list()
    for sensor in listaSensores:
        lectura=lecturaSensor(sensor, ik)
        listaLecturas.append(lectura)
        print('Lectura obtenida: '+ str(lectura) + ' '+ factor.get_unidad())
    lecturaPromedio= sum(listaLecturas) / len(listaLecturas)
    print('Lectura promedio: '+str(lecturaPromedio))
    return lecturaPromedio

def crearFactor(factor): #DESPUES
    return None

def eliminarFactor(idFactor): #DESPUES
    return None

def crearGrupoActuadores(grupoActuadores): #DESPUES
    return None

def eliminarGrupoActuadores(idGrupoActuadores): #DESPUES
    return None
    

if __name__ == '__main__':
    __placa=iniciarPlaca()
    ikPlaca= instanciarIK(__placa.get_nro_serie())
    ikPlaca.waitForAttach(10000)
    listaFactores= __placa.get_lista_factores()
    for factor in listaFactores:
        procesarLecturaFactor(factor, ikPlaca)
            
    try:
        ikPlaca.closePhidget()
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Exiting....4")
            
            
    
    
    