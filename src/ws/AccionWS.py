# -*- encoding: utf-8 -*-
from soaplib.serializers.clazz import ClassSerializer
from soaplib.serializers.primitive import  Integer, String


class AccionWS(ClassSerializer):
    """
    Clase utilizada para convertir a un objeto serializable un resultado lectura para enviarlo en respuesta a una llamada de web service.
    """
    class types:
        idAccion= Integer
        fecha=String
        tipoAccion=String
        idDispositivo=Integer

    def __init__(self, idAccion, fecha, tipoAccion, idDispositivo):
        """Constructor de la clase LecturaWS."""
        self.idAccion= idAccion
        self.fecha = fecha
        self.tipoAccion = tipoAccion
        self.idDispositivo = idDispositivo

    def get_id_accion(self):
        """
        @rtype: Integer
        @return: Devuelve el identificador de la accion."""
        return self.idAccion
    
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

    def get_tipo_accion(self):
        """
        @rtype: String
        @return: Devuelve el tipo de accion ejecutado.""" 
        return self.tipoAccion

    def set_tipo_accion(self, value):
        """Asigna un identificador a la lectura"""
        self.tipoAccion = value
    
    def set_fecha(self, value):
        """Asigna un Datetime como fecha y hora en que se genera el ResultadoLectura"""
        self.fecha = value

    def set_id_dispositivo(self, value):
        """Asigna un int como el identificado del factor sobre el que se obtiene la lectura."""
        self.idDispositivo = value


