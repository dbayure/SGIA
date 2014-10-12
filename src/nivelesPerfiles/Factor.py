# -*- encoding: utf-8 -*-
class Factor(object):
    """
    La clase factor se utiliza para nuclear sensores de un mismo tipo, por ejemplo temperatura.
    Posee métodos que permiten manejar las lecturas de un grupo de sensores, así como asignarles su unidad correspondiente.
    Abstrae la lectura de las particularidades de cada sensor. Es utilizado directamente para obtener lecturas, y para
    establecer los rangos de las mismas a considerar en cada nivel de severidad.
    Sus atributos son: idFactor, nombre, unidad, la lista de sensores que lo componen, y activoSistema que maneja su estado lógico en el sistema.
    """
    
    __idFactor= None
    __nombre=None
    __unidad=None
    __valorMin= None
    __valorMax= None
    __umbral= None
    __listaSensores= None
    __activoSistema= None

    def __init__(self, idFactor, nombre, unidad, valorMin, valorMax, umbral, listaSensores, activoSistema):
        """
        Constructor de la clase factor.
        @type idFactor: int
        @param idFactor: Identificador del factor.
        @type nombre: String
        @param nombre: Nombre del factor.
        @type unidad: String
        @param unidad: Unidad de lectura del factor.
        @type valorMin: int
        @param valorMin: Valor mínimo admitido como normal para el factor.
        @type valorMax: int
        @param valorMax: Valor máximo admitido como normal para el factor.
        @type umbral: int
        @param umbral: Umbral de diferencia permitido entre dos lecturas del mismo factor.
        @type listaSensores: List<Sensor>
        @param listaSensores: Lista de sensores asociados al factor.
        @type activoSistema: Char(1)
        @param activoSistema: Indicador si el factor está activo en el sistema (S/N)"""
        self.__idFactor = idFactor
        self.__nombre = nombre
        self.__unidad = unidad
        self.__valorMin= valorMin
        self.__valorMax= valorMax
        self.__umbral= umbral
        self.__listaSensores = listaSensores
        self.__activoSistema = activoSistema

    def get_id_factor(self):
        """
        @rtype: int
        @return: Devuelve el identificador de un factor"""
        return self.__idFactor

    def get_nombre(self):
        """
        @rtype: String
        @return: Devuelve el nombre de un factor."""
        return self.__nombre

    def get_unidad(self):
        """
        @rtype: String
        @return: Devuelve la unidad de un factor."""
        return self.__unidad
    
    def get_umbral(self):
        """
        @rtype: int
        @return: Devuelve el umbral de diferencia permitido entre lecturas"""
        return self.__umbral

    def get_lista_sensores(self):
        """
        @rtype: List<Sensor>
        @return: Devuelve la lista de sensores que pertenece al factor."""
        return self.__listaSensores

    def get_activo_sistema(self):
        """
        @rtype: Char(1)
        @return: Devuelve el estado lógico en el sistema de un factor (S/N)"""
        return self.__activoSistema

    def set_id_factor(self, value):
        """Asigna un int como identificador de un factor"""
        self.__idFactor = value

    def set_nombre(self, value):
        """Asigna un String como nombre de un factor"""
        self.__nombre = value

    def set_unidad(self, value):
        """Asigna un String como unidad de un factor"""
        self.__unidad = value
        
    def set_umbral(self, value):
        """Asigna un int como el umbral de diferencia permitido entre lecturas"""
        self.__umbral= value

    def set_lista_sensores(self, value):
        """Asigna una List<Sensor> como la lista de sensores de un factor."""
        self.__listaSensores = value

    def set_activo_sistema(self, value):
        """Asigna el estado del factor en el sistema, recibe un Char(1)
        Los estados pueden ser: A= Activo, E= Eliminado"""
        self.__activoSistema = value
        
    def get_valor_min(self):
        """
        @rtype: int
        @return: Devuelve el valor mínimo permitido para el factor"""
        return self.__valorMin

    def get_valor_max(self):
        """
        @rtype: int
        @return: Devuelve el valor máximo permitido para el factor"""
        return self.__valorMax

    def set_valor_min(self, value):
        """Asigna un int como el valor mínimo permitido para el factor"""
        self.__valorMin = value

    def set_valor_max(self, value):
        """Asigna un int como el valor máximo permitido para el factor"""
        self.__valorMax = value

    idFactor = property(get_id_factor, set_id_factor, None, None)
    nombre = property(get_nombre, set_nombre, None, None)
    unidad = property(get_unidad, set_unidad, None, None)
    listaSensores = property(get_lista_sensores, set_lista_sensores, None, None)
    activoSistema = property(get_activo_sistema, set_activo_sistema, None, None)
    valorMin = property(get_valor_min, set_valor_min, None, None)
    valorMax = property(get_valor_max, set_valor_max, None, None)
        