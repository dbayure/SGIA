# -*- encoding: utf-8 -*-
"""
Módulo principal del sistema, es el encargado de iniciar la ejecución del mismo.
Debe instanciar la placa y el servidor de WS, además es encargado de comunicarse con la 
capa de persistencia para guardar y recuperar datos.
Tiene como atributos una instancia única de placa y una instancia única de ws.
"""
from src.bdd.ManejadorBD import ManejadorBD

__placa=None
__ws=None

def iniciarPlaca():
    """
    Método que inicializa la placa controladora y carga sus estructuras desde la BD
    """
    mbd= ManejadorBD()
    con= mbd.getConexion()
    estado= mbd.obtenerEstadoPlaca(con)
    nroSerie= mbd.obtenerNroSeriePlaca(con)
    listaDispositivos= mbd.obtenerListaDispositivos(con)
    listaFactores= mbd.obtenerListaFactores(con)
    for factor in listaFactores:
        idFactor= factor.get_id_factor()
        listaSensores= list()
        listaIdSensores=mbd.obtenerListaIdSensoresFactor(con, idFactor)
        for idSensor in listaIdSensores:
            i=0
            while idSensor <>listaDispositivos[i].get_id_dispositivo():
                i= i+1
            sensor= listaDispositivos[i]
            listaSensores.append(sensor)
        factor.set_lista_sensores(listaSensores)
    #aca la lista de factores ya está actualizada con la lista de sensores de cada una
            
    
    
    print('Se obtuvieron '+str(len(listaDispositivos))+' dispositivos')
    for dispositivo in listaDispositivos:
        print(dispositivo.get_nombre())
        print(dispositivo.get_modelo())
        if dispositivo.get_modelo() == '1014':
            lista=dispositivo.get_lista_dispositivos()
            actuador=lista[0]
            print(actuador.get_modelo())
        
    
    
    
    mbd.cerrarConexion()
    print "estado obtenido ", estado
    print "nro serie obtenido ", nroSerie
    return None

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

def lecturaSensor(idDispositivo):
    return None

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

def procesarLecturaFactor(idFactor): 
    return None

def crearFactor(factor): #DESPUES
    return None

def eliminarFactor(idFactor): #DESPUES
    return None

def crearGrupoActuadores(grupoActuadores): #DESPUES
    return None

def eliminarGrupoActuadores(idGrupoActuadores): #DESPUES
    return None
    

if __name__ == '__main__':
    iniciarPlaca()