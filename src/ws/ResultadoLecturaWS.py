# -*- encoding: utf-8 -*-
from soaplib.serializers.clazz import ClassSerializer
from soaplib.serializers.primitive import DateTime, Integer
from src.logs.Mensaje import Mensaje

class ResultadoLecturaWS(ClassSerializer):
    """
    Clase utilizada para convertir a un objeto serializable un resultado lectura para enviarlo en respuesta
    a una llamada de web service
    """
    class types:
        mensaje=Mensaje
        fecha=DateTime
        idFactor=Integer
        valor=Integer

    def __init__(self, mensaje, fecha, idFactor, valor):
        self.mensaje = mensaje
        self.fecha = fecha
        self.idFactor = idFactor
        self.valor = valor

    def get_mensaje(self):
        return self.__mensaje

    def get_fecha(self):
        return self.__fecha

    def get_id_factor(self):
        return self.__idFactor

    def get_valor(self):
        return self.__valor

    def set_mensaje(self, value):
        self.__mensaje = value

    def set_fecha(self, value):
        self.__fecha = value

    def set_id_factor(self, value):
        self.__idFactor = value

    def set_valor(self, value):
        self.__valor = value
   
