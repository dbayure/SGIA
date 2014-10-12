# -*- encoding: utf-8 -*-
from soaplib.serializers.clazz import ClassSerializer
from soaplib.serializers.primitive import Integer
from src.logs.Mensaje import Mensaje

class ResultadoCreacionWS(ClassSerializer):
    """
    Clase utilizada para Devolver el identificador de un objeto creado y un mensaje asociado al procedimiento
    """
    class types:
        mensaje=Mensaje
        idObjeto=Integer

    def __init__(self, mensaje, idObjeto):
        """Constructor de la clase ResultadoCreacionWS.
        @type mensaje: Mensaje
        @param mensaje: Mensaje asociado a creación del objeto.
        @type idObjeto: int
        @param idObjeto: Identificador del objeto creado"""
        self.mensaje = mensaje
        self.idObjeto = idObjeto

    def get_mensaje(self):
        """
        @rtype: Mensaje
        @return: Devuelve el mensaje asociado a la creación del objeto."""
        return self.__mensaje

    def get_id_objeto(self):
        """
        @rtype: int
        @return: Devuelve el identificador del objeto creado."""
        return self.__idObjeto

    def set_mensaje(self, value):
        """Asigna un Mensaje como el mensaje asociado a la creación del objeto."""
        self.__mensaje = value

    def set_id_objeto(self, value):
        """Asigna un int como identificador del objeto creado."""
        self.__idObjeto = value

    mensaje = property(get_mensaje, set_mensaje, None, None)
    idObjeto = property(get_id_objeto, set_id_objeto, None, None)
