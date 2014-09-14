# -*- encoding: utf-8 -*-
class Factor(object):
    """
    La clase factor se utiliza para nuclear sensores de un mismo tipo, por ejemplo temperatura.
    Posee métodos que permiten manejar las lecturas de un grupo de sensores, así como asignarles su unidad correspondiente.
    Abstrae la lectura de las particularidades de cada sensor. Es utilizado directamente para obtener lecturas, y para
    establecer los rangos de las mismas a considerar en cada nivel de severidad.
    Sus atributos son: idFactor, nombre, unidad, la lista de sensores que lo componen, y activoSistema que maneja
    su estado lógico en el sistema.
    """
    
    __idFactor= None
    __nombre=None
    __unidad=None
    __valorMin= None
    __valorMax= None
    __periodicidad= None
    __listaSensores= None
    __activoSistema= None

    def __init__(self, idFactor, nombre, unidad, valorMin, valorMax, listaSensores, activoSistema):
        """
        Constructor de la clase factor, recibe como parámetros:
        -idFactor: int
        -nombre: String
        -unidad: String
        -valorMin: int
        -valorMax: int
        -listaSensores: List<Sensor>
        -activoSistema: Char(1)
        """
        self.__idFactor = idFactor
        self.__nombre = nombre
        self.__unidad = unidad
        self.__valorMin= valorMin
        self.__valorMax= valorMax
        self.__listaSensores = listaSensores
        self.__activoSistema = activoSistema

    def get_id_factor(self):
        """
        Devuelve el id de un factor como un int
        """
        return self.__idFactor


    def get_nombre(self):
        """
        Devuelve el nombre de un factor como un String
        """
        return self.__nombre


    def get_unidad(self):
        """
        Devuelve la unidad de un factor como un String
        """
        return self.__unidad


    def get_lista_sensores(self):
        """
        Devuelve la lista de sensores que componen un factor como un List<Sensor>
        """
        return self.__listaSensores


    def get_activo_sistema(self):
        """
        Devuelve el estado lógico en el sistema de un factor como un Char(1)
        """
        return self.__activoSistema


    def set_id_factor(self, value):
        """
        Asigna un int como id de un factor
        """
        self.__idFactor = value


    def set_nombre(self, value):
        """
        Asigna un String como nombre de un factor
        """
        self.__nombre = value


    def set_unidad(self, value):
        """
        Asigna un String como unidad de un factor
        """
        self.__unidad = value


    def set_lista_sensores(self, value):
        """
        Asigna un List<Sensor> como la lista de sensores de un factor
        """
        self.__listaSensores = value


    def set_activo_sistema(self, value):
        """
        Asigna el estado del factor en el sistema, recibe un Char(1)
        Los estados pueden ser: A= Activo, E= Eliminado
        """
        self.__activoSistema = value
        
    def get_valor_min(self):
        return self.__valorMin


    def get_valor_max(self):
        return self.__valorMax


    def set_valor_min(self, value):
        self.__valorMin = value


    def set_valor_max(self, value):
        self.__valorMax = value

    idFactor = property(get_id_factor, set_id_factor, None, None)
    nombre = property(get_nombre, set_nombre, None, None)
    unidad = property(get_unidad, set_unidad, None, None)
    listaSensores = property(get_lista_sensores, set_lista_sensores, None, None)
    activoSistema = property(get_activo_sistema, set_activo_sistema, None, None)
    valorMin = property(get_valor_min, set_valor_min, None, None)
    valorMax = property(get_valor_max, set_valor_max, None, None)

    

    




    
        