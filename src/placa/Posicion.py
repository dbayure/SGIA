# -*- encoding: utf-8 -*-
class Posicion(object):
    """
    La clase Posición es utilizada para representar las posiciones que puede tener un actuador de avance.
    Cada posición tiene una lista de sensores que determinan su cumplimiento según un valor definido para tal fin.
    """

    __posicion= None
    __descripcion= None
    __valor= None
    __listaSensores= None
            
    def __init__(self, posicion, descripcion, valor, listaSensores):
        """Constructor de la clase Posicion.
        @type posicion: int
        @param posicion: Número que identifica la posición
        @type descripcion: String
        @param descripcion: Descripción de la posición
        @type valor: int
        @param valor: Valor que determina el cumplimiento de la posición
        @type listaSensores: List<Sensor>
        @param listaSensores: Lista de sensores que controlan el cumplimiento de la posición."""
        self.__posicion = posicion
        self.__descripcion = descripcion
        self.__valor = valor
        self.__listaSensores = listaSensores

    def get_posicion(self):
        """
        @rtype: int
        @return: Devuelve el número que identifica a la posición"""
        return self.__posicion

    def get_descripcion(self):
        """
        @rtype: String
        @return: Devuelve la descripción de la posición"""
        return self.__descripcion

    def get_valor(self):
        """
        @rtype: int
        @return: Devuelve el valor que indica el cumplimiento de la posición"""
        return self.__valor

    def get_lista_sensores(self):
        """
        @rtype: List<Sensor>
        @return: Devuelve la lista de sensores que determinan el cumplimiento de la posición"""
        return self.__listaSensores

    def set_posicion(self, value):
        """Asigna un int como el número que identifica a la posición"""
        self.__posicion = value

    def set_descripcion(self, value):
        """Asigna un String como la descripción de la posición"""
        self.__descripcion = value

    def set_valor(self, value):
        """Asigna un int como el valor a partir del cual se cumple la posición"""
        self.__valor = value

    def set_lista_sensores(self, value):
        """Asigna un List<Sensor> como la lista de sensores que determina el cumplimiento de la posición."""
        self.__listaSensores = value

    posicion = property(get_posicion, set_posicion, None, None)
    descripcion = property(get_descripcion, set_descripcion, None, None)
    valor = property(get_valor, set_valor, None, None)
    listaSensores = property(get_lista_sensores, set_lista_sensores, None, None)
