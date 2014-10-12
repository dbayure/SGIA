# -*- encoding: utf-8 -*-

class NivelSeveridad(object):
    """
    Clase utilizada para definir un nivel de severidad del sistema, en base al que se activará un perfil de activación asociado al mismo.
    """

    __idNivel= None
    __nombre= None
    __factor= None
    __prioridad= None
    __rangoMinimo= None
    __rangoMaximo= None
    __perfilActivacion= None
    __activoSistema= None

    def __init__(self, idNivel, nombre, factor, prioridad, rangoMinimo, rangoMaximo, perfilActivacion, activoSistema):
        """Constructor de un Nivel de severidad.
        @type idNivel: int
        @param idNivel: Identificador de un nivel de severidad
        @type nombre: String
        @param nombre: Nombre del nivel de severidad.
        @type factor: Factor
        @param factor: Factor sobre el que se determina el nivel de severidad
        @type prioridad: int
        @param prioridad: Prioridad de aplicación del nivel de severidad (a menor valor mayor prioridad)
        @type rangoMinimo: int
        @param rangoMinimo: Valor mínimo para determinar el rango de cumplimiento 
        @type rangoMaximo: int
        @param rangoMaximo: Valor máximo para determinar el rango de cumplimiento
        @type perfilActivacion: PerfilActivacion
        @param perfilActivacion: Perfil de activación asociado al nivel de severidad"""
        self.__idNivel = idNivel
        self.__nombre = nombre
        self.__factor = factor
        self.__prioridad = prioridad
        self.__rangoMinimo = rangoMinimo
        self.__rangoMaximo = rangoMaximo
        self.__perfilActivacion = perfilActivacion
        self.__activoSistema = activoSistema
        
    def __cmp__( self, other ) :
        """Método utilizado para comparación de dos niveles de severidad según su prioridad"""
        if self.__prioridad < other.__prioridad :
            rst = -1
        elif self.__prioridad > other.__prioridad :
            rst = 1
        else :
            rst = 0
        return rst

    def get_id_nivel(self):
        """
        @rtype: int
        @return: Devuelve el identificador de un nivel de severidad"""
        return self.__idNivel

    def get_nombre(self):
        """
        @rtype: String
        @return: Devuelve el nombre de un nivel de severidad"""
        return self.__nombre

    def get_factor(self):
        """
        @rtype: Factor
        @return: Devuelve el factor sobre el que se determina el nivel de severidad"""
        return self.__factor

    def get_prioridad(self):
        """
        @rtype: int
        @return: Devuelve la prioridad de aplicación del nivel de severidad"""
        return self.__prioridad

    def get_rango_minimo(self):
        """
        @rtype: int
        @return: Devuelve el valor mínimo que determina el rango de cumplimiento del nivel de severidad."""
        return self.__rangoMinimo

    def get_rango_maximo(self):
        """
        @rtype: int
        @return: Devuelve el valor máximo que determina el rango de cumplimiento del nivel de severidad."""
        return self.__rangoMaximo

    def get_perfil_activacion(self):
        """
        @rtype: PerfilActivacion
        @return: Devuelve el perfil de activación asociado al nivel de severidad."""
        return self.__perfilActivacion

    def set_id_nivel(self, value):
        """Asigna un int como identificador de un nivel de severidad"""
        self.__idNivel = value

    def set_nombre(self, value):
        """Asigna un String como nombre de un nivel de severidad."""
        self.__nombre = value

    def set_factor(self, value):
        """Asigna un factor como el factor sobre el que actua el nivel de severidad"""
        self.__factor = value

    def set_prioridad(self, value):
        """Asigna un int como la prioridad de aplicación de un nivel de severidad"""
        self.__prioridad = value

    def set_rango_minimo(self, value):
        """Asigna un int como el valor mínimo que determina el rango en el que se cumple el nivel de severidad""" 
        self.__rangoMinimo = value

    def set_rango_maximo(self, value):
        """Asigna un int como el valor máximo que determina el rango en el que se cumple el nivel de severidad"""
        self.__rangoMaximo = value

    def set_perfil_activacion(self, value):
        """Asigna un PerfilActivacion como el perfil de activación asociado a un nivel de severidad"""
        self.__perfilActivacion = value
    
    def get_activo_sistema(self):
        """
        @rtype: char(1)
        @return: Devuelve si el nivel de severidad está activo en el sistema. (S/N)"""
        return self.__activoSistema

    def set_activo_sistema(self, value):
        """Asigna un char(1) como indicador si el nivel de severidad está activo en el sistema. (S/N)"""
        self.__activoSistema = value

    idNivel = property(get_id_nivel, set_id_nivel, None, None)
    nombre = property(get_nombre, set_nombre, None, None)
    factor = property(get_factor, set_factor, None, None)
    prioridad = property(get_prioridad, set_prioridad, None, None)
    rangoMinimo = property(get_rango_minimo, set_rango_minimo, None, None)
    rangoMaximo = property(get_rango_maximo, set_rango_maximo, None, None)
    perfilActivacion = property(get_perfil_activacion, set_perfil_activacion, None, None)
    activoSistema = property(get_activo_sistema, set_activo_sistema, None, None)
