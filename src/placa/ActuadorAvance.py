# -*- encoding: utf-8 -*-
from src.placa.Dispositivo import Dispositivo

class ActuadorAvance(Dispositivo):
    """
    La clase ActuadorAvance se utiliza para representar un dispositivo de tipo actuador de avance.
    Además de los atributos de un dispositivo tiene una posición que determina en que estado de avance está el actuador, puede tener un estado de retroceso y un puerto asociado para lograr este efecto, 
    un tipoActuador de tipo tipoActuador, por ejemplo, cortinas, un atributo tipoPuerto que indica si está conectado a un puerto analógico, digital de entrada ó digital de salida y un tiempo de tolerancia 
    para transición entre dos posiciones consecutivas.
    """
    __posicion= None
    __tipoActuador= None
    __tipoPuerto= None
    __numeroPuertoRetroceso= None
    __tipoPuertoRetroceso= None
    __tiempoEntrePosiciones= None
    __listaPosiciones= None

    def __init__(self, idDispositivo, nombre, modelo, numeroPuerto, activoSistema, padre, estadoAlerta, posicion, tipoActuador, tipoPuerto, numeroPuertoRetroceso, tipoPuertoRetroceso, tiempoEntrePosiciones, listaPosiciones):
        """Constructor de un actuador de avance.
        @type idDispositivo: int
        @param idDispositivo: Identificador del actuador
        @type nombre: String
        @param nombre: Nombre del dispositivo
        @type modelo: String
        @param modelo: Modelo del dispositivo
        @type numeroPuerto: int
        @param numeroPuerto: Número de puerto al que está conectado el dispositivo
        @type activoSistema: Char(1)
        @param activoSistema: Indicador del estado del dispositivo en el sistema. (S/N)
        @type padre: int
        @param padre: Identificador del dispositivo padre
        @type posicion: int
        @param posicion: Posición en la que se encuentra el actuador de avance.
        @type tipoActuador: TipoActuador
        @param tipoActuador: Tipo de actuador al que pertenece el actuador de avance.
        @type tipoPuerto: TipoPuerto
        @param tipoPuerto: Tipo de puerto al que está conectado el actuador de avance.
        @type numeroPuertoRetroceso: int
        @param numeroPuertoRetroceso: Número del puerto de retroceso al que está conectado el actuador de avance
        @type tipoPuertoRetroceso: TipoPuerto
        @param tipoPuerto: Tipo de puerto de retroceso al que está conectado el actuador de avance.
        @type tiempoEntrePosiciones: int
        @param tiempoEntrePosiciones: Tiempo permitido para transición entre dos posiciones consecutivas
        @type listaPosiciones: List<Posicion>
        @param listaPosiciones: Lista de posiciones que posee el actuador de avance."""
        Dispositivo.__init__(self, idDispositivo, nombre, modelo, numeroPuerto, activoSistema, padre, estadoAlerta)
        self.__posicion = posicion
        self.__tipoActuador = tipoActuador
        self.__tipoPuerto = tipoPuerto
        self.__numeroPuertoRetroceso = numeroPuertoRetroceso
        self.__tipoPuertoRetroceso = tipoPuertoRetroceso
        self.__tiempoEntrePosiciones = tiempoEntrePosiciones
        self.__listaPosiciones = listaPosiciones

    def get_posicion(self):
        """
        @rtype: int
        @return: Devuelve la posición actual del actuador de avance"""
        return self.__posicion

    def get_tipo_actuador(self):
        """
        @rtype: TipoActuador
        @return: Devuelve el tipo de actuador del actuador de avance"""
        return self.__tipoActuador

    def get_tipo_puerto(self):
        """
        @rtype: TipoPuerto
        @return: Devuelve el tipo de puerto al que está conectado el actuador de avance."""
        return self.__tipoPuerto

    def get_numero_puerto_retroceso(self):
        """
        @rtype: int
        @return: Devuelve el numero del puerto de retroceso al que está conectado el actuador de avance."""
        return self.__numeroPuertoRetroceso

    def get_tipo_puerto_retroceso(self):
        """
        @rtype: TipoPuerto
        @return: Devuelve el tipo de puerto de retroceso al que está conectado el actuador de avance."""
        return self.__tipoPuertoRetroceso

    def get_tiempo_entre_posiciones(self):
        """
        @rtype: int
        @return: Devuelve el tiempo permitido para transición entre dos posiciones consecutivas"""
        return self.__tiempoEntrePosiciones

    def get_lista_posiciones(self):
        """
        @rtype: List<Posicion>
        @return: Devuelve la lista de posiciones que posee el actuador de avance"""
        return self.__listaPosiciones

    def set_posicion(self, value):
        """Asigna un int como posición actual de un actuador de avance."""
        self.__posicion = value

    def set_tipo_actuador(self, value):
        """Asigna un TipoActuador como tipo de actuador del actuador de avance"""
        self.__tipoActuador = value

    def set_tipo_puerto(self, value):
        """Asigna un TipoPuerto como tipo de puerto al que está conectado el actuador de avance"""
        self.__tipoPuerto = value

    def set_numero_puerto_retroceso(self, value):
        """Asigna un int como el número de puerto de retroceso al que está conectado un actuador de avance"""
        self.__numeroPuertoRetroceso = value

    def set_tipo_puerto_retroceso(self, value):
        """Asigna un TipoPuerto como el tipo de puerto de retroceso al que está conectado el actuador de avance"""
        self.__tipoPuertoRetroceso = value

    def set_tiempo_entre_posiciones(self, value):
        """Asigna un int como el tiempo permitido para transición entre dos posiciones consecutivas"""
        self.__tiempoEntrePosiciones = value

    def set_lista_posiciones(self, value):
        """Asigna una List<Posicion> como la lista de posiciones que posee el actuador de avance"""
        self.__listaPosiciones = value

    posicion = property(get_posicion, set_posicion, None, None)
    tipoActuador = property(get_tipo_actuador, set_tipo_actuador, None, None)
    tipoPuerto = property(get_tipo_puerto, set_tipo_puerto, None, None)
    numeroPuertoRetroceso = property(get_numero_puerto_retroceso, set_numero_puerto_retroceso, None, None)
    tipoPuertoRetroceso = property(get_tipo_puerto_retroceso, set_tipo_puerto_retroceso, None, None)
    tiempoEntrePosiciones = property(get_tiempo_entre_posiciones, set_tiempo_entre_posiciones, None, None)
    listaPosiciones = property(get_lista_posiciones, set_lista_posiciones, None, None)
    