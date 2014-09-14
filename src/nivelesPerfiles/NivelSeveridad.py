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
        """Constructor de un Nivel de severidad. Recibe como parámetros:
        -idNivel: int
        -nombre: String
        -factor: Factor
        -prioridad: int
        -rangoMinimo: int
        -rangoMaximo: int
        -perfilActivacion: PerfilActivacion"""
        self.__idNivel = idNivel
        self.__nombre = nombre
        self.__factor = factor
        self.__prioridad = prioridad
        self.__rangoMinimo = rangoMinimo
        self.__rangoMaximo = rangoMaximo
        self.__perfilActivacion = perfilActivacion
        self.__activoSistema = activoSistema
        
    def __cmp__( self, other ) :
        if self.__prioridad < other.__prioridad :
            rst = -1
        elif self.__prioridad > other.__prioridad :
            rst = 1
        else :
            rst = 0
        return rst

    def get_id_nivel(self):
        return self.__idNivel


    def get_nombre(self):
        return self.__nombre


    def get_factor(self):
        return self.__factor


    def get_prioridad(self):
        return self.__prioridad


    def get_rango_minimo(self):
        return self.__rangoMinimo


    def get_rango_maximo(self):
        return self.__rangoMaximo


    def get_perfil_activacion(self):
        return self.__perfilActivacion


    def set_id_nivel(self, value):
        self.__idNivel = value


    def set_nombre(self, value):
        self.__nombre = value


    def set_factor(self, value):
        self.__factor = value


    def set_prioridad(self, value):
        self.__prioridad = value


    def set_rango_minimo(self, value):
        self.__rangoMinimo = value


    def set_rango_maximo(self, value):
        self.__rangoMaximo = value


    def set_perfil_activacion(self, value):
        self.__perfilActivacion = value
    
    def get_activo_sistema(self):
        return self.__activoSistema


    def set_activo_sistema(self, value):
        self.__activoSistema = value

    idNivel = property(get_id_nivel, set_id_nivel, None, None)
    nombre = property(get_nombre, set_nombre, None, None)
    factor = property(get_factor, set_factor, None, None)
    prioridad = property(get_prioridad, set_prioridad, None, None)
    rangoMinimo = property(get_rango_minimo, set_rango_minimo, None, None)
    rangoMaximo = property(get_rango_maximo, set_rango_maximo, None, None)
    perfilActivacion = property(get_perfil_activacion, set_perfil_activacion, None, None)
    activoSistema = property(get_activo_sistema, set_activo_sistema, None, None)

    

    
        