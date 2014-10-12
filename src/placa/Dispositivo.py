# -*- encoding: utf-8 -*-

class Dispositivo(object):
    """
    clase abstracta que contiene los atributos y funciones básicas de los dispositivos.
    Sus especializaciones serán "actuador", "actuadorAvance", "sensor" y "placaAuxiliar"
    Sus atributos son: idDispositivo, nombre, modelo, numeroPuerto, padre, activoSistema y estadoAlerta
    """
        
    __idDispositivo= None
    __nombre= None
    __modelo= None
    __numeroPuerto= None
    __activoSistema= None  
    __padre= None
    __estadoAlerta= None

    def __init__(self, idDispositivo, nombre, modelo, numeroPuerto, activoSistema, padre, estadoAlerta):
        """Constructor de un dispositivo.
        @type idDispositivo: int
        @param idDispositivo: Identificador del actuador
        @type nombre: String
        @param nombre: Nombre del dispositivo
        @type modelo: String
        @param modelo: Modelo del dispositivo
        @type numeroPuerto: int
        @param numeroPuerto: Número de puerto al que está conectado el dispositivo
        @type activoSistema: Char(1)
        @param activoSistema: Indicador del estado del dispositivo en el sistema. (S/N)
        @type padre: int
        @param padre: Identificador del dispositivo padre
        @type estadoAlerta: Char(1)
        @param estadoAlerta: Indicador si el dispositivo está en estado de alerta. (S/N)"""
        self.__idDispositivo = idDispositivo
        self.__nombre = nombre
        self.__modelo = modelo
        self.__numeroPuerto = numeroPuerto
        self.__activoSistema = activoSistema
        self.__padre = padre
        self.__estadoAlerta= estadoAlerta

    def get_id_dispositivo(self):
        """
        @rtype: int
        @return: Devuelve el identificador de un dispositivo"""
        return self.__idDispositivo

    def get_nombre(self):
        """
        @rtype: String
        @return: Devuelve el nombre del dispositivo"""
        return self.__nombre

    def get_modelo(self):
        """
        @rtype: String
        @return: Devuelve el modelo del dispositivo"""
        return self.__modelo

    def get_numero_puerto(self):
        """
        @rtype: int
        @return: Devuelve el numero de puerto en el que esta conectado el dispositivo"""
        return self.__numeroPuerto

    def get_activo_sistema(self):
        """
        @rtype: Char(1)
        @return: Devuelve el estado del dispositivo en el sistema, estos pueden ser: A= Activo, E= Eliminado"""
        return self.__activoSistema
    
    def get_padre(self):
        """
        @rtype: int
        @return: Devuelve identificador del dispositivo padre"""
        return self.__padre
    
    def get_estado_alerta(self):
        """
        @rtype: 
        @return: Devuelve si el dispositivo esta en estado de alerta (S/N)"""
        return self.__estadoAlerta

    def set_id_dispositivo(self, value):
        """Asigna un int como identificador del dispositivo"""
        self.__idDispositivo = value

    def set_nombre(self, value):
        """Asigna un String como nombre del dispositivo"""
        self.__nombre = value

    def set_modelo(self, value):
        """Asigna un String como modelo del dispositivo"""
        self.__modelo = value

    def set_numero_puerto(self, value):
        """Asigna un int como número de puerto en el que esta conectado el dispositivo"""
        self.__numeroPuerto = value

    def set_activo_sistema(self, value):
        """Asigna un char(1) como el estado del dispositivo en el sistema. Los estados pueden ser: A= Activo, E= Eliminado"""
        self.__activoSistema = value
        
    def set_estado_alerta(self, value):
        """Asigna un char(1) como indicador del estado de alerta del dispositivo (S/N)"""
        self.__estadoAlerta = value
        
    def set_padre(self, value):
        """Asigna un char(1) como el estado del dispositivo en el sistema, estos pueden ser: A= Activo, E= Eliminado"""
        self.__padre = value

    idDispositivo = property(get_id_dispositivo, set_id_dispositivo, None, None)
    nombre = property(get_nombre, set_nombre, None, None)
    modelo = property(get_modelo, set_modelo, None, None)
    numeroPuerto = property(get_numero_puerto, set_numero_puerto, None, None)
    activoSistema = property(get_activo_sistema, set_activo_sistema, None, None)
    padre = property(get_padre, set_padre, None, None)
