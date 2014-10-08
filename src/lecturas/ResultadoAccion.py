# -*- encoding: utf-8 -*-
from src.lecturas.Resultado import Resultado

class ResultadoAccion(Resultado):
    """
    La clase ResultadoAccion hereda de la clase Resultado, se utiliza para retornar un resultado
    luego de una acción sobre un dispositivo actuador o sobre la placa controladora.
    Sus atributos son: el id del actuador o dispositivo sobre el que se disparó la acción, el tipo de acción
    y la fecha en la que se produjo la acción.
    """

    __idGrupoActuadores=None
    __tipoAccion=None
    

    def __init__(self, mensaje, fecha, idGrupoActuadores, tipoAccion):
        """Constructor de la clase ResultadoAccion
            @type idGrupoActuadores: int
            @param idGrupoActuadores: Id del grupo de actuadores que disparó la acción 
            @type tipoAccion: String
            @param tipoAccion: Tipo de acción disparada."""
        Resultado.__init__(self, mensaje, fecha)
        self.__idGrupoActuadores = idGrupoActuadores
        self.__tipoAccion = tipoAccion

    def get_id_grupo_actuadores(self):
        """
        @rtype: int
        @return: Devuelve el id de dispositivo de un ResultadoAccion como un int"""
        return self.__idGrupoActuadores

    def get_tipo_accion(self):
        """
        @rtype: String
        @return: Devuelve el tipo de acción de un ResultadoAccion como un String"""
        return self.__tipoAccion

    def set_id_grupo_actuadores(self, value):
        """Asigna un int como id de dispositivo asociado a un ResultadoAccion"""
        self.__idDispositivo = value

    def set_tipo_accion(self, value):
        """Asigna un String como tipo de accion de un ResultadoAccion"""
        self.__tipoAccion = value

    idGrupoActuadores = property(get_id_grupo_actuadores, set_id_grupo_actuadores, None, None)
    tipoAccion = property(get_tipo_accion, set_tipo_accion, None, None)
    