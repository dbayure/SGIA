# -*- encoding: utf-8 -*-
from soaplib.serializers.clazz import ClassSerializer
from soaplib.serializers.primitive import DateTime, Integer
from src.logs.Mensaje import Mensaje

class ResultadoLecturaWS(ClassSerializer):
    """
    Clase utilizada para convertir a un objeto serializable un resultado lectura para enviarlo en respuesta a una llamada de web service.
    """
    class types:
        mensaje=Mensaje
        fecha=DateTime
        idFactor=Integer
        valor=Integer

    def __init__(self, mensaje, fecha, idFactor, valor):
        """Constructor de la clase ResultadoLecturaWS.
        @type mensaje: Mensaje
        @param mensaje: Mensaje asociado al resultado de la lectura.
        @type fecha: Datetime
        @param fecha: Fecha y hora en que se genera el ResultadoLectura
        @type idFactor: int
        @param idFactor: Identificador del factor que genera la lectura.
        @type valor: float
        @param valor: Valor de lectura obtenido."""
        self.mensaje = mensaje
        self.fecha = fecha
        self.idFactor = idFactor
        self.valor = valor

    def get_mensaje(self):
        """
        @rtype: Mensaje
        @return: Devuelve el mensaje asociado al ResultadoLectura."""
        return self.__mensaje

    def get_fecha(self):
        """
        @rtype: Datetime
        @return: Devuelve la fecha y hora en la que se produce el ResultadoLectura."""
        return self.__fecha

    def get_id_factor(self):
        """
        @rtype: int
        @return: Devuelve el identificador del factor que genera la lectura"""
        return self.__idFactor

    def get_valor(self):
        """
        @rtype: float
        @return: Devuelve el valor obtenido por la lectura.""" 
        return self.__valor

    def set_mensaje(self, value):
        """Asigna un Mensaje como el mensaje asociado al ResultadoLectura"""
        self.__mensaje = value

    def set_fecha(self, value):
        """Asigna un Datetime como fecha y hora en que se genera el ResultadoLectura"""
        self.__fecha = value

    def set_id_factor(self, value):
        """Asigna un int como el identificado del factor sobre el que se obtiene la lectura."""
        self.__idFactor = value

    def set_valor(self, value):
        """Asigna un float como el valor obtenido en la lectura."""
        self.__valor = value
