# -*- encoding: utf-8 -*-
from Phidgets.PhidgetException import PhidgetException
class Placa(object):
    """
    Clase utilizada para instanciar el objeto placa controladora, se creará una instancia única de esta.
    Tiene como atributos su número de serie, el estado del sistema, las periodicidades de lectura y procesado de niveles de severidad,
    la lista de dispositivos conectados directamente a ella, la lista de niveles de severidad definidos por el usuario, las listas de grupos de actuadores
    y factores formadas por los distintos dispositivos con los que debe interactuar el sistema, y el interfaceKit que instancia para interactuar con los demás dispositivos.
    """
    
    __nroSerie=None
    __estadoSistema=None
    __periodicidadLecturas= None
    __periodicidadNiveles= None
    __listaDispositivos=None
    __listaGrupoActuadores=None
    __listaFactores= None
    __listaNivelesSeveridad= None
    __ik= None
    __estadoAlerta= None
    
    def __init__(self, nroSerie, estadoSistema, periodicidadLecturas, periodicidadNiveles, listaDispositivos, listaGrupoActuadores, listaFactores, listaNivelesSeveridad, estadoAlerta):
        """
        Constructor de la clase placa.
        @type nroSerie: String
        @param nroSerie: Número de serie de la placa controladora
        @type estadoSistema: Char(1)
        @param estadoSistema: Estado del sistema, estos pueden ser: I=Inactivo, C=Configuración, M=Manual ó A=Automático
        @type periodicidadLecturas: int
        @param periodicidadLecturas: Tiempo en segundos establecido como la periodicidad en que se toman lecturas automáticamente
        @type periodicidadNiveles: int
        @param periodicidadNiveles: Tiempo en segundos establecido como la periodicidad en que se procesan los niveles de severidad
        @type listaDispositivos: List<Dispositivo>
        @param listaDispositivos: Lista de dispositivos conectados directamente a la placa controladora.
        @type listaGrupoActuadores: List<GrupoActuador> 
        @param listaGrupoActuadores:  Lista de grupos de actuadores definidos en el sistema 
        @type listaFactores: List<Factor>
        @param listaFactores: Lista de factores definidos en el sistema
        @type listaNivelesSeveridad: List<NivelSeveridad>
        @param listaNivelesSeveridad: Lista de niveles de severidad definidos en el sistema
        @type estadoAlerta: Char(1)
        @param estadoAlerta: Indicador si existe algun dispositivo en el sistema en estado de alerta
        """
        self.__nroSerie = nroSerie
        self.__estadoSistema = estadoSistema
        self.__periodicidadLecturas= periodicidadLecturas
        self.__periodicidadNiveles= periodicidadNiveles
        self.__listaDispositivos = listaDispositivos
        self.__listaGrupoActuadores = listaGrupoActuadores
        self.__listaFactores = listaFactores
        self.__listaNivelesSeveridad= listaNivelesSeveridad
        self.__estadoAlerta= estadoAlerta
        
    def get_nro_serie(self):
        """
        @rtype: String
        @return: Devuelve el número de serie de la placa controladora."""
        return self.__nroSerie

    def get_estado_sistema(self):
        """
        @rtype: Char(1)
        @return: Devuelve el estado del sistema, estos pueden ser: I=Inactivo, C=Configuración, M=Manual o A=Automático"""
        return self.__estadoSistema

    def get_lista_dispositivos(self):
        """
        @rtype: List<Dispositivo>
        @return: Devuelve la lista de dispositivos conectados directamente a la placa controladora."""
        return self.__listaDispositivos

    def get_lista_grupo_actuadores(self):
        """
        @rtype: List<GrupoActuador>
        @return: Devuelve la lista de grupos de actuadores definidos en el sistema."""
        return self.__listaGrupoActuadores

    def get_lista_factores(self):
        """
        @rtype: List<Factor>
        @return: Devuelve la lista de factores definidos en el sistema."""
        return self.__listaFactores
    
    def get_ik(self):
        """
        @rtype: InterfaceKit
        @return: Devuelve el interface kit de la placa controladora."""
        return self.__ik
    
    def get_estado_alerta(self):
        """
        @rtype: Char(1)
        @return: Devuelve si existe algun dispositivo en el sistema en estado de alerta (S/N)"""
        return self.__estadoAlerta

    def set_nro_serie(self, value):
        """Asigna un String como número de serie de la placa controladora."""
        self.__nroSerie = value

    def set_estado_sistema(self, value):
        """Asigna un Char(1) como estado del sistema, estos pueden ser: I=Inactivo, C=Configuración, M=Manual o A=Automático"""
        self.__estadoSistema = value

    def set_lista_dispositivos(self, value):
        """Asigna un List<Dispositivo> como la lista de dispositivos conectados directamente a la placa controladora."""
        self.__listaDispositivos = value

    def set_lista_grupo_actuadores(self, value):
        """Asigna un List<GrupoActuadores> como la lista de grupos de actuadores definidos en el sistema."""
        self.__listaGrupoActuadores = value

    def set_lista_factores(self, value):
        """Asigna un List<Factor> como la lista de factores definidos en el sistema."""
        self.__listaFactores = value
        
    def set_ik(self, value):
        """Asigna un Interfacekit a la placa controladora."""
        self.__ik = value
        
    def set_estado_alerta(self, value):
        """Asigna un char(1) como el estado alerta del sistema."""
        self.__estadoAlerta = value
        
    def cerrarIK(self):
        """Método para cerrar la conexión al interface kit instanciado por la placa controladora."""
        try:
            self.ik.closePhidget()
        except PhidgetException as e:
            print("Phidget Exception %i: %s" % (e.code, e.details))
            print("Exiting....4")
            
    def __del__(self):
        """Método invocado automáticamente al destruir una instancia de la clase, se asegura que se cierre la conexión al interface kit instanciado"""
        if self.__ik <> None:
            self.cerrarIK() 
            
    def get_lista_niveles_severidad(self):
        """
        @rtype: List<NivelSeveridad>
        @return: Devuelve la lista de niveles de severidad definidos en el sistema."""
        return self.__listaNivelesSeveridad

    def set_lista_niveles_severidad(self, value):
        """Asigna una List<NivelSeveridad> como la lista de niveles de severidad del sistema."""
        self.__listaNivelesSeveridad = value
        
    def get_periodicidad_lecturas(self):
        """
        @rtype: int
        @return: Devuelve el tiempo en segundos establecido como periodicidad para tomar lecturas automáticamente."""
        return self.__periodicidadLecturas

    def get_periodicidad_niveles(self):
        """
        @rtype: int
        @return: Devuelve el tiempo en segundos establecido como periodicidad para tomar procesar los niveles de severidad automáticamente."""
        return self.__periodicidadNiveles

    def set_periodicidad_lecturas(self, value):
        """Asigna un int como la periodicidad en segundos para tomar lecturas automáticamente."""
        self.__periodicidadLecturas = value

    def set_periodicidad_niveles(self, value):
        """Asigna un int como la periodicidad en segundos para procesar los niveles de severidad automáticamente."""
        self.__periodicidadNiveles = value

    nroSerie = property(get_nro_serie, set_nro_serie, None, None)
    estadoSistema = property(get_estado_sistema, set_estado_sistema, None, None)
    listaDispositivos = property(get_lista_dispositivos, set_lista_dispositivos, None, None)
    listaGrupoActuadores = property(get_lista_grupo_actuadores, set_lista_grupo_actuadores, None, None)
    listaFactores = property(get_lista_factores, set_lista_factores, None, None)
    ik = property(get_ik, set_ik, None, None)
    listaNivelesSeveridad = property(get_lista_niveles_severidad, set_lista_niveles_severidad, None, None)
    periodicidadLecturas = property(get_periodicidad_lecturas, set_periodicidad_lecturas, None, None)
    periodicidadNiveles = property(get_periodicidad_niveles, set_periodicidad_niveles, None, None)
    estadoAlerta = property(get_estado_alerta, set_estado_alerta, None, None)
    