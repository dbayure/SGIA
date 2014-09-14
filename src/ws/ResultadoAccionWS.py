# -*- encoding: utf-8 -*-
from soaplib.serializers.clazz import ClassSerializer
from soaplib.serializers.primitive import DateTime, Integer, String
from src.logs.Mensaje import Mensaje

class ResultadoAccionWS(ClassSerializer):
    """
    Clase utilizada para convertir a un objeto serializable un resultado lectura para enviarlo en respuesta
    a una llamada de web service
    """
    class types:
        mensaje=Mensaje
        fecha=DateTime
        idGrupoActuadores=Integer
        tipoAccion=String

    def __init__(self, mensaje, fecha, idGrupoActuadores, tipoAccion):
        self.mensaje = mensaje
        self.fecha = fecha
        self.idGrupoActuadores = idGrupoActuadores
        self.tipoAccion = tipoAccion

    def get_mensaje(self):
        return self.__mensaje


    def get_fecha(self):
        return self.__fecha


    def get_id_grupo_actuadores(self):
        return self.__idGrupoActuadores


    def get_tipo_accion(self):
        return self.__tipoAccion


    def set_mensaje(self, value):
        self.__mensaje = value


    def set_fecha(self, value):
        self.__fecha = value


    def set_id_grupo_actuadores(self, value):
        self.__idGrupoActuadores = value


    def set_tipo_accion(self, value):
        self.__tipoAccion = value

    mensaje = property(get_mensaje, set_mensaje, None, None)
    fecha = property(get_fecha, set_fecha, None, None)
    idGrupoActuadores = property(get_id_grupo_actuadores, set_id_grupo_actuadores, None, None)
    tipoAccion = property(get_tipo_accion, set_tipo_accion, None, None)

    