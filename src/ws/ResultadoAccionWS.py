# -*- encoding: utf-8 -*-
from soaplib.serializers.clazz import ClassSerializer
from soaplib.serializers.primitive import DateTime, Integer, String
from src.logs.Mensaje import Mensaje

class ResultadoAccionWS(ClassSerializer):
    """
    Clase utilizada para convertir a un objeto serializable un resultado lectura para enviarlo en respuesta a una llamada de web service
    """
    class types:
        mensaje=Mensaje
        fecha=DateTime
        idGrupoActuadores=Integer
        tipoAccion=String

    def __init__(self, mensaje, fecha, idGrupoActuadores, tipoAccion):
        """
        Constructor de la clase ResultadoAccion.
        @type mensaje: Mensaje
        @param mensaje: Mensaje enviado en el ResultadoAccion
        @type fecha: Datetime
        @param fecha: Fecha y hora en que se genera el ResultadoAccion
        @type idGrupoActuadores: int
        @param idGrupoActuadores: Identificador del grupo de actuadores que dispara la acción
        @type tipoAccion: Char(1)
        @param tipoAccion: Acción que ejecuta el grupo de actuadores."""
        self.mensaje = mensaje
        self.fecha = fecha
        self.idGrupoActuadores = idGrupoActuadores
        self.tipoAccion = tipoAccion

    def get_mensaje(self):
        """
        @rtype: Mensaje
        @return: Devuelve el mensaje emitido en el ResultadoAccion"""
        return self.__mensaje

    def get_fecha(self):
        """
        @rtype: Datetime
        @return: Devuelve la fecha y hora en que se genera el ResultadoAccion"""
        return self.__fecha

    def get_id_grupo_actuadores(self):
        """
        @rtype: int
        @return: Devuelve el identificador del grupo de actuadores que dispara la acción."""
        return self.__idGrupoActuadores

    def get_tipo_accion(self):
        """
        @rtype: Char(1)
        @return: Devuelve la acción disparada por el grupo de actuadores."""
        return self.__tipoAccion

    def set_mensaje(self, value):
        """Asigna un Mensaje como el mensaje asociado al ResultadoAccion"""
        self.__mensaje = value

    def set_fecha(self, value):
        """Asigna un Datetime como la fecha y hora en que se genera el ResultadoAccion"""
        self.__fecha = value

    def set_id_grupo_actuadores(self, value):
        """Asigna un int como el identificador del grupo de actuadores que disparó la acción"""
        self.__idGrupoActuadores = value

    def set_tipo_accion(self, value):
        """Asigna un char(1) como el tipo de acción del ResultadoAcción"""
        self.__tipoAccion = value

    mensaje = property(get_mensaje, set_mensaje, None, None)
    fecha = property(get_fecha, set_fecha, None, None)
    idGrupoActuadores = property(get_id_grupo_actuadores, set_id_grupo_actuadores, None, None)
    tipoAccion = property(get_tipo_accion, set_tipo_accion, None, None)
