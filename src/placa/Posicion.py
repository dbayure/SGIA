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
        self.__posicion = posicion
        self.__descripcion = descripcion
        self.__valor = valor
        self.__listaSensores = listaSensores

    def get_posicion(self):
        return self.__posicion


    def get_descripcion(self):
        return self.__descripcion


    def get_valor(self):
        return self.__valor


    def get_lista_sensores(self):
        return self.__listaSensores


    def set_posicion(self, value):
        self.__posicion = value


    def set_descripcion(self, value):
        self.__descripcion = value


    def set_valor(self, value):
        self.__valor = value


    def set_lista_sensores(self, value):
        self.__listaSensores = value

    posicion = property(get_posicion, set_posicion, None, None)
    descripcion = property(get_descripcion, set_descripcion, None, None)
    valor = property(get_valor, set_valor, None, None)
    listaSensores = property(get_lista_sensores, set_lista_sensores, None, None)

