# -*- encoding: utf-8 -*-
class GrupoActuadores(object):
    """
    La clase GrupoActuadores se utiliza para nuclear actuadores de un mismo tipo, que deben ejecutar su encendido o apagado en paralelo, por ejemplo, todos los ventiladores.
    Son utilizados para recibir órdenes manuales de encendido o apagado, ó listados en los perfiles de activación
    para actuar de determinada manera sobre estos ante el cumplimiento del nivel de severidad asociado.
    Sus atributos son: idGrupoActuador, estado (que puede ser encendido o apagado), nombre, listaActuadores, y activoSistema que indica su estado lógico en el sistema.
    """
    
    __idGrupoActuador=None
    __estado=None
    __nombre=None
    __listaActuadores=None
    __deAvance= None
    __activoSistema=None

    def __init__(self, idGrupoActuador, estado, nombre, listaActuadores, deAvance, activoSistema):
        """
        Constructor de la clase GrupoActuador.
        @type idGrupoActuador: int
        @param idGrupoActuador: Identificador de un grupo de actuadores
        @type estado: char(1)
        @param estado: Estado actual del grupo de actuadores, puede ser A=Apagado, E=Encendido, ó un número que se corresponde con el número de posición para un grupo de actuadores de avance.
        @type nombre: String
        @param nombre: Nombre del grupo de actuadores.
        @type listaActuadores: List<Dispositivo>
        @param listaActuadores: Lista de actuadores que componen el grupo de actuadores, pueden ser actuadores ó actuadores de avance.
        @type deAvance: char(1)
        @param deAvance: Indica si se trata de un grupo de actuadores de avance o no (S/N)
        @type activoSistema: char(1)
        @param activoSistema: Indica si el grupo de actuadores está activo en el sistema (S/N)"""
        self.__idGrupoActuador = idGrupoActuador
        self.__estado = estado
        self.__nombre = nombre
        self.__listaActuadores = listaActuadores
        self.__deAvance= deAvance
        self.__activoSistema = activoSistema

    def get_id_grupo_actuador(self):
        """
        @rtype: int
        @return: Devuelve el identificador de un GrupoActuador"""
        return self.__idGrupoActuador

    def get_estado(self):
        """
        @rtype: char(1)
        @return: Devuelve el estado actual del grupo de actuadores."""
        return self.__estado

    def get_nombre(self):
        """
        @rtype: String
        @return: Devuelve el nombre de un GrupoActuador"""
        return self.__nombre

    def get_lista_actuadores(self):
        """
        @rtype: List<Dispositivo>
        @return: Devuelve la lista de actuadores de un GrupoActuador."""
        return self.__listaActuadores
    
    def get_de_avance(self):
        """
        @rtype: char(1)
        @return: Devuelve la lista de actuadores de un GrupoActuador"""
        return self.__deAvance

    def get_activo_sistema(self):
        """
        @rtype: char(1)
        @return: Devuelve el estado lógico en el sistema de un GrupoActuador."""
        return self.__activoSistema

    def set_id_grupo_actuador(self, value):
        """Asigna un int como identificador de un GrupoActuador"""
        self.__idGrupoActuador = value

    def set_estado(self, value):
        """Asigna un char(1) como estado de un GrupoActuador, estos pueden ser A=Apagado, E=Encendido para grupo de actuadores común, o un número para grupo de actuadores de avance, que se corresponde con el número de posición actual."""
        self.__estado = value

    def set_nombre(self, value):
        """Asigna un String como nombre de un GrupoActuador"""
        self.__nombre = value

    def set_lista_actuadores(self, value):
        """Asigna una List<Dispositivo> como la lista de actuadores de un GrupoActuador"""
        self.__listaActuadores = value

    def set_de_avance(self, value):
        """Asigna un char(1) como indicador si se trata de un GrupoActuador de avance o no. (S/N)"""
        self.__deAvance = value

    def set_activo_sistema(self, value):
        """Asigna un char(1) como estado lógico del GrupoActuador en el sistema."""
        self.__activoSistema = value

    idGrupoActuador = property(get_id_grupo_actuador, set_id_grupo_actuador, None, None)
    estado = property(get_estado, set_estado, None, None)
    nombre = property(get_nombre, set_nombre, None, None)
    listaActuadores = property(get_lista_actuadores, set_lista_actuadores, None, None)
    activoSistema = property(get_activo_sistema, set_activo_sistema, None, None)
    deAvance= property(get_de_avance, set_de_avance, None, None)
        