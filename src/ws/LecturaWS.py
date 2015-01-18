# -*- encoding: utf-8 -*-
from soaplib.serializers.clazz import ClassSerializer
from soaplib.serializers.primitive import  Integer, Float, String


class LecturaWS(ClassSerializer):
    """
    Clase utilizada para convertir a un objeto serializable un resultado lectura para enviarlo en respuesta a una llamada de web service.
    """
    class types:
        idLectura= Integer
        fecha=String
        lectura=Float
        idDispositivo=Integer

    def __init__(self, idLectura, fecha, lectura, idDispositivo):
        """Constructor de la clase LecturaWS."""
        self.idLectura= idLectura
        self.fecha = fecha
        self.lectura = lectura
        self.idDispositivo = idDispositivo

    def get_id_lectura(self):
        """
        @rtype: Integer
        @return: Devuelve el identificador de la lectura."""
        return self.idLectura
    
    def get_fecha(self):
        """
        @rtype: String
        @return: Devuelve la fecha y hora en la que se produce el ResultadoLectura."""
        return self.fecha

    def get_id_dispositivo(self):
        """
        @rtype: int
        @return: Devuelve el identificador del factor que genera la lectura"""
        return self.idDispositivo

    def get_lectura(self):
        """
        @rtype: float
        @return: Devuelve el valor obtenido por la lectura.""" 
        return self.lectura

    def set_id_lectura(self, value):
        """Asigna un identificador a la lectura"""
        self.idLectura = value
    
    def set_fecha(self, value):
        """Asigna un Datetime como fecha y hora en que se genera el ResultadoLectura"""
        self.fecha = value

    def set_id_dispositivo(self, value):
        """Asigna un int como el identificado del factor sobre el que se obtiene la lectura."""
        self.idDispositivo = value

    def set_lectura(self, value):
        """Asigna un float como el valor obtenido en la lectura."""
        self.lectura = value
