"""
Módulo principal del sistema, es el encargado de iniciar la ejecución del mismo.
Debe instanciar la placa y el servidor de WS, además es encargado de comunicarse con la 
capa de persistencia para guardar y recuperar datos.
Tiene como atributos una instancia única de placa y una instancia única de ws.
"""

__placa=None
__ws=None

def iniciarPlaca():
    return None

def iniciarWS():
    return None

def cambiarEstadoPlaca(estado):
    return None

def chequeoPlaca():
    return None

def chequeoDispositivo(idDispositivo):
    return None

def chequeoDispositivos():
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

def cargarNivelPerfil(nivelSeveridad, perfilActivacion):
    return None

def eliminarNivelPerfil (idNivelSeveridad):
    return None

def cargarDispositivo (dispositivo):
    return None

def eliminarDispositivo (idDispositivo):
    return None

def iniciarComportamientoAutomatico():
    return None

def detenerComportamientoAutomatico(control):
    return None

def iniciarChequeosAutomaticos():
    return None

def procesarLecturaFactor(idFactor):
    return None

def crearFactor(factor):
    return None

def eliminarFactor(idFactor):
    return None

def crearGrupoActuadores(grupoActuadores):
    return None

def eliminarGrupoActuadores(idGrupoActuadores):
    return None
    

if __name__ == '__main__':
    pass