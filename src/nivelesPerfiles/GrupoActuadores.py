class GrupoActuadores(object):
    """
    La clase GrupoActuadores se utiliza para nuclear actuadores de un mismo tipo, que deben ejecutar
    su encendido o apagado en paralelo, por ejemplo, todos los ventiladores.
    Son utilizados para recibir órdenes manuales de encendido o apagado, ó listados en los perfiles de activación
    para actuar de determinada manera sobre estos ante el cumplimiento del nivel de severidad asociado.
    Sus atributos son: idGrupoActuador, estado (que puede ser encendido o apagado), nombre, listaActuadores, y activoSistema
    que indica su estado lógico en el sistema.
    """
    
    __idGrupoActuador=None
    __estado=None
    __nombre=None
    __listaActuadores=None
    __activoSistema=None

    def __init__(self, idGrupoActuador, estado, nombre, listaActuadores, activoSistema):
        """
        Constructor de la clase GrupoActuador, recibe como parámetros:
        -idGrupoActuador: int
        -estado: int
        -nombre: String
        -listaActuadores: List<Actuador>
        -activoSistema: Char(1)
        """
        self.__idGrupoActuador = idGrupoActuador
        self.__estado = estado
        self.__nombre = nombre
        self.__listaActuadores = listaActuadores
        self.__activoSistema = activoSistema

    def get_id_grupo_actuador(self):
        """
        Devuelve el id de un GrupoActuador como un int
        """
        return self.__idGrupoActuador


    def get_estado(self):
        """
        Devuelve el estado (1= Encendido, 0=Apagado) de un GrupoActuador como un int
        """
        return self.__estado


    def get_nombre(self):
        """
        Devuelve el nombre de un GrupoActuador como un String
        """
        return self.__nombre


    def get_lista_actuadores(self):
        """
        Devuelve la lista de actuadores de un GrupoActuador como un List<Actuador>
        """
        return self.__listaActuadores


    def get_activo_sistema(self):
        """
        Devuelve el estado lógico en el sistema de un GrupoActuador como un Char(1)
        """
        return self.__activoSistema


    def set_id_grupo_actuador(self, value):
        """
        Asigna un int como id de un GrupoActuador
        """
        self.__idGrupoActuador = value


    def set_estado(self, value):
        """
        Asigna un int como estado de un GrupoActuador, estos puede ser: 1= Encendido, 0=Apagado
        """
        self.__estado = value


    def set_nombre(self, value):
        """
        Asigna un String como nombre de un GrupoActuador
        """
        self.__nombre = value


    def set_lista_actuadores(self, value):
        """
        Asigna un List<Actuador> como la lista de actuadores de un GrupoActuador
        """
        self.__listaActuadores = value


    def set_activo_sistema(self, value):
        """
        Asigna el estado del GrupoActuador en el sistema, recibe un Char(1)
        Los estados pueden ser: A= Activo, E= Eliminado
        """
        self.__activoSistema = value

    idGrupoActuador = property(get_id_grupo_actuador, set_id_grupo_actuador, None, None)
    estado = property(get_estado, set_estado, None, None)
    nombre = property(get_nombre, set_nombre, None, None)
    listaActuadores = property(get_lista_actuadores, set_lista_actuadores, None, None)
    activoSistema = property(get_activo_sistema, set_activo_sistema, None, None)



    
        