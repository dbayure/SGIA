# -*- encoding: utf-8 -*-
"""Modulo "dispositivo" contiene la definición de la clase dispositivo"""

class Dispositivo(object):
    """
    clase abstracta que contiene los atributos y funciones básicas de los dispositivos.
    Sus especializaciones serán "actuador", "sensor" y "placaAuxiliar"
    Sus atributos son:
        -idDispositivo
        -nombre
        -modelo
        -numeroPuerto
        -activoSistema
    """
        
    __idDispositivo= None
    __nombre= None
    __modelo= None
    __numeroPuerto= None
    __activoSistema= None  
    __padre= None
    __estadoAlerta= None

    def __init__(self, idDispositivo, nombre, modelo, numeroPuerto, activoSistema, padre, estadoAlerta):
        """
        Constructor de un dispositivo, recibe como parámetros:
            -idDispositivo : int
            -nombre: String
            -modelo: String
            -numeroPuerto: int
            -activoSistema: Boolean
            -estadoAlerta: Char(1)
        """
        self.__idDispositivo = idDispositivo
        self.__nombre = nombre
        self.__modelo = modelo
        self.__numeroPuerto = numeroPuerto
        self.__activoSistema = activoSistema
        self.__padre = padre
        self.__estadoAlerta= estadoAlerta

    def get_id_dispositivo(self):
        """
        Devuelve idDispositivo como un int
        """
        return self.__idDispositivo


    def get_nombre(self):
        """
        Devuelve el nombre del dispositivo como un String
        """
        return self.__nombre


    def get_modelo(self):
        """
        Devuelve el modelo del dispositivo como un String
        """
        return self.__modelo


    def get_numero_puerto(self):
        """
        Devuelve el numero de puerto en el que esta el dispositivo como un int
        """
        return self.__numeroPuerto


    def get_activo_sistema(self):
        """
        Devuelve el estado del dispositivo en el sistema, como un char(1)
        Los estados pueden ser: A= Activo, E= Eliminado
        """
        return self.__activoSistema
    
    def get_padre(self):
        """
        Devuelve idDispositivo como un int
        """
        return self.__padre
    
    def get_estado_alerta(self):
        """
        Devuelve si el dispositivo esta en estado de alerta
        """
        return self.__estadoAlerta


    def set_id_dispositivo(self, value):
        """
        Asigna un id de dispositivo, recibe un int
        """
        self.__idDispositivo = value


    def set_nombre(self, value):
        """
        Asigna un nombre al dispositivo, recibe un String
        """
        self.__nombre = value


    def set_modelo(self, value):
        """
        Asigna un modelo al dispositivo, recibe un String
        """
        self.__modelo = value


    def set_numero_puerto(self, value):
        """
        Asigna un numero de puerto en el que esta conectado el dispositivo, recibe un int
        """
        self.__numeroPuerto = value


    def set_activo_sistema(self, value):
        """
        Asigna el estado del dispositivo en el sistema, recibe un Char(1)
        Los estados pueden ser: A= Activo, E= Eliminado
        """
        self.__activoSistema = value
        
    def set_estado_alerta(self, value):
        """
        Asigna el estado de alerta del dispositivo
        """
        self.__estadoAlerta = value
        
    def set_padre(self, value):
        """
        Asigna el estado del dispositivo en el sistema, recibe un Char(1)
        Los estados pueden ser: A= Activo, E= Eliminado
        """
        self.__padre = value

    idDispositivo = property(get_id_dispositivo, set_id_dispositivo, None, None)
    nombre = property(get_nombre, set_nombre, None, None)
    modelo = property(get_modelo, set_modelo, None, None)
    numeroPuerto = property(get_numero_puerto, set_numero_puerto, None, None)
    activoSistema = property(get_activo_sistema, set_activo_sistema, None, None)
    padre = property(get_padre, set_padre, None, None)
