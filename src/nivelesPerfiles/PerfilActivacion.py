# -*- encoding: utf-8 -*-

class PerfilActivacion(object):
    """
    Clase utilizada para definir los perfiles de activación de una lista de grupo de actuadores ante el cumplimiento de 
    un nivel de severidad al cual está asociado el perfil de activación
    """
    
    __idPerfilActivacion= None
    __listaGrupoActuadoresEstado= None


    def __init__(self, idPerfilActivacion, listaGrupoActuadoresEstado):
        """Constructor de la clase PerfilActivacion, recibe como parámetros:
        -idPerfilActivacion: int
        -listaGrupoActuadores: List<(GrupoActuadores, Char(1))>
        """
        self.__idPerfilActivacion = idPerfilActivacion
        self.__listaGrupoActuadoresEstado = listaGrupoActuadoresEstado


    def get_id_perfil_activacion(self):
        return self.__idPerfilActivacion


    def get_lista_grupo_actuadores_estado(self):
        return self.__listaGrupoActuadoresEstado


    def set_id_perfil_activacion(self, value):
        self.__idPerfilActivacion = value


    def set_lista_grupo_actuadores_estado(self, value):
        self.__listaGrupoActuadoresEstado = value

    idPerfilActivacion = property(get_id_perfil_activacion, set_id_perfil_activacion, None, None)
    listaGrupoActuadoresEstado = property(get_lista_grupo_actuadores_estado, set_lista_grupo_actuadores_estado, None, None)


        