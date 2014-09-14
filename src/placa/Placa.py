# -*- encoding: utf-8 -*-
from Phidgets.PhidgetException import PhidgetException
from src.recursos.Herramientas import Herramientas
class Placa(object):
    """
    Clase utilizada para instanciar el objeto placa controladora, se creará una instancia única de esta.
    Tiene como atributos su número de serie, el estado del sistema, la lista de dispositivos conectados 
    directamente a ella, la lista de niveles de severidad definidos por el usuario y las listas de grupos de actuadores
    y factores formadas por los distintos dispositivos con los que debe interactuar el sistema.
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
    
    
    def __init__(self, nroSerie, estadoSistema, periodicidadLecturas, periodicidadNiveles, listaDispositivos, listaGrupoActuadores, listaFactores, listaNivelesSeveridad):
        """
        Constructor de la clase placa, recibe como parámetros:
            -nroSerie : String
            -estadoSistema: Char(1), estos pueden ser: I=Inactivo, C=Configuración, M=Manual o A=Automático
            -periodicidadLecturas: int (segundos)
            -periodicidadNiveles: int (segundos)
            -listaDispositivos: List<Dispositivo>
            -listaGrupoActuadores: List<GrupoActuadores>
            -listaFactores: List<Factor>
        """
        self.__nroSerie = nroSerie
        self.__estadoSistema = estadoSistema
        self.__periodicidadLecturas= periodicidadLecturas
        self.__periodicidadNiveles= periodicidadNiveles
        self.__listaDispositivos = listaDispositivos
        self.__listaGrupoActuadores = listaGrupoActuadores
        self.__listaFactores = listaFactores
        self.__listaNivelesSeveridad= listaNivelesSeveridad
        
 

    def get_nro_serie(self):
        """
        Devuelve el número de serie de la placa como un String
        """
        return self.__nroSerie


    def get_estado_sistema(self):
        """
        Devuelve el estado del sistema como un Char(1), estos pueden ser:
        I=Inactivo, C=Configuración, M=Manual o A=Automático
        """
        return self.__estadoSistema


    def get_lista_dispositivos(self):
        """
        Devuelve la lista de dispositivos conectados directamente a la placa como un List<Dispositivo>
        """
        return self.__listaDispositivos


    def get_lista_grupo_actuadores(self):
        """
        Devuelve la lista de grupos de actuadores como un List<GrupoActuadores>
        """
        return self.__listaGrupoActuadores


    def get_lista_factores(self):
        """
        Devuelve la lista de factores como un List<Factor>
        """
        return self.__listaFactores
    
    def get_ik(self):
        """
        Devuelve el interface kit de la placa
        """
        return self.__ik


    def set_nro_serie(self, value):
        """
        Asigna un String como número de serie de la placa
        """
        self.__nroSerie = value


    def set_estado_sistema(self, value):
        """
        Asigna un Char(1) como estado del sistema, estos pueden ser:
        I=Inactivo, C=Configuración, M=Manual o A=Automático
        """
        self.__estadoSistema = value


    def set_lista_dispositivos(self, value):
        """
        Asigna un List<Dispositivo> como la lista de dispositivos conectados a la placa.
        """
        self.__listaDispositivos = value


    def set_lista_grupo_actuadores(self, value):
        """
        Asigna un List<GrupoActuadores> como la lista de grupos de actuadores definidos en el sistema.
        """
        self.__listaGrupoActuadores = value


    def set_lista_factores(self, value):
        """
        Asigna un List<Factor> como la lista de factores definidos en el sistema.
        """
        self.__listaFactores = value
        
    def set_ik(self, value):
        """
        Asigna un interface kit a la placa controladora
        """
        self.__ik = value
        
    def cerrarIK(self):
        try:
            self.ik.closePhidget()
        except PhidgetException as e:
            print("Phidget Exception %i: %s" % (e.code, e.details))
            print("Exiting....4")
            
    def __del__(self):
        if self.__ik <> None:
            self.cerrarIK() 
            
    def get_lista_niveles_severidad(self):
        return self.__listaNivelesSeveridad


    def set_lista_niveles_severidad(self, value):
        self.__listaNivelesSeveridad = value
        
    def get_periodicidad_lecturas(self):
        return self.__periodicidadLecturas


    def get_periodicidad_niveles(self):
        return self.__periodicidadNiveles


    def set_periodicidad_lecturas(self, value):
        self.__periodicidadLecturas = value


    def set_periodicidad_niveles(self, value):
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
    

    

        