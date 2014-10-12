# -*- encoding: utf-8 -*-

class PerfilActivacion(object):
    """
    Clase utilizada para definir los perfiles de activación, los cuales están formados por una lista de grupo de actuadores  y los estados en que deben estar estos, 
    ante el cumplimiento de un nivel de severidad al cual está asociado el perfil de activación.
    """
    
    __idPerfilActivacion= None
    __listaGrupoActuadoresEstado= None


    def __init__(self, idPerfilActivacion, listaGrupoActuadoresEstado):
        """Constructor de la clase PerfilActivacion.
        @type idPerfilActivacion: int
        @param idPerfilActivacion: Identificador del perfil de activación.
        @type listaGrupoActuadoresEstado: List<(GrupoActuadores, Char(1))>
        @param listaGrupoActuadoresEstado: Lista de tuplas compuestas por un grupo de actuadores y el estado en el que debe estar este ante el cumplimiento de un nivel de severidad"""
        self.__idPerfilActivacion = idPerfilActivacion
        self.__listaGrupoActuadoresEstado = listaGrupoActuadoresEstado

    def get_id_perfil_activacion(self):
        """
        @rtype: int
        @return: Devuelve el identificador del perfil de activación"""
        return self.__idPerfilActivacion

    def get_lista_grupo_actuadores_estado(self):
        """
        @rtype: List<(GrupoActuadores, Char(1))>
        @return: Devuelve la lista de tuplas compuestas por un grupo de actuadores y el estado en el que debe estar este ante el cumplimiento de un nivel de severidad"""
        return self.__listaGrupoActuadoresEstado

    def set_id_perfil_activacion(self, value):
        """Asigna un int como identificador del perfil de activación"""
        self.__idPerfilActivacion = value

    def set_lista_grupo_actuadores_estado(self, value):
        """Asigna una List<(GrupoActuadores, Char(1))> como la lista de grupos de actuadores y sus respectivos estados."""
        self.__listaGrupoActuadoresEstado = value

    idPerfilActivacion = property(get_id_perfil_activacion, set_id_perfil_activacion, None, None)
    listaGrupoActuadoresEstado = property(get_lista_grupo_actuadores_estado, set_lista_grupo_actuadores_estado, None, None)
