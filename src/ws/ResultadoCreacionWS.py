# -*- encoding: utf-8 -*-
from soaplib.serializers.clazz import ClassSerializer
from soaplib.serializers.primitive import Integer
from src.logs.Mensaje import Mensaje

class ResultadoCreacionWS(ClassSerializer):
    """
    Clase utilizada para Devolver el id de objeto creado y un mensaje asociado al procedimiento
    """
    class types:
        mensaje=Mensaje
        idObjeto=Integer

    def __init__(self, mensaje, idObjeto):
        self.mensaje = mensaje
        self.idObjeto = idObjeto

    def get_mensaje(self):
        return self.__mensaje


    def get_id_objeto(self):
        return self.__idObjeto


    def set_mensaje(self, value):
        self.__mensaje = value


    def set_id_objeto(self, value):
        self.__idObjeto = value

    mensaje = property(get_mensaje, set_mensaje, None, None)
    idObjeto = property(get_id_objeto, set_id_objeto, None, None)

        