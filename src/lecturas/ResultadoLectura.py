# -*- encoding: utf-8 -*-
from src.lecturas.Resultado import Resultado

class ResultadoLectura(Resultado):
    """
    La clase ResultadoLectura hereda de la clase Resultado, se utiliza para retornar un resultado
    luego de una lectura sobre un sensor.
    Sus atributos son: el id del dispositivo sensor sobre el que se efectuó la lectura y el valor obtenido de la misma
    """

    __idDispositivo=None
    __valor=None

    def __init__(self, mensaje, fecha, idDispositivo, valor):
        """
        Constructor de la clase ResultadoLectura, recibe como parámetros:
            -mensaje: Mensaje (Resultado)
            -fecha: Date (Resultado)
            -idDispositivo: int (ResultadoLectura)
            -valor: float (ResultadoLectura)
        """
        Resultado.__init__(self, 
            mensaje, fecha)
        self.__idDispositivo = idDispositivo
        self.__valor = valor

    def get_id_dispositivo(self):
        """
        Devuelve el id de dispositivo de un ResultadoLectura como un int
        """
        return self.__idDispositivo


    def get_valor(self):
        """
        Devuelve el valor obtenido en un ResultadoLectura como un float
        """
        return self.__valor


    def set_id_dispositivo(self, value):
        """
        Asigna un int como id de dispositivo asociado a un ResultadoLectura
        """
        self.__idDispositivo = value


    def set_valor(self, value):
        """
        Asigna un float como valor de lectura obtenido en un ResultadoLectura
        """
        self.__valor = value

    idDispositivo = property(get_id_dispositivo, set_id_dispositivo, None, None)
    valor = property(get_valor, set_valor, None, None)

    
    
        