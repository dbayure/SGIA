# -*- encoding: utf-8 -*-
from src.placa.Dispositivo import Dispositivo

class Actuador(Dispositivo):
    """
    La clase actuador se utiliza para representar un dispositivo de tipo actuador.
    Además de los atributos de un dispositivo tiene un estadoActuador de tipo Char(1), que puede ser E= Encendido ó A= Apagado, un tipoActuador de tipo tipoActuador,
    por ejemplo, ventilador, y un atributo tipoPuerto que indica si está conectado a un puerto analógico, digital de entrada ó digital de salida.
    """
    __estadoActuador= None
    __tipoActuador= None
    __tipoPuerto= None

    def __init__(self, idDispositivo, nombre, modelo, numeroPuerto, activoSistema, padre, estadoAlerta, estado, tipoActuador, tipoPuerto):
        """
        Constructor de un actuador.
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
        @type estadoAlerta: Char(1)
        @param estadoAlerta: Indicador si el dispositivo está en estado de alerta. (S/N)
        @type tipoActuador: TipoActuador
        @param tipoActuador: Tipo de actuador al que pertenece el actuador.
        @type tipoPuerto: TipoPuerto
        @param tipoPuerto: Tipo de puerto al que está conectado el actuador."""
        Dispositivo.__init__(self, idDispositivo, nombre, modelo, numeroPuerto, activoSistema, padre, estadoAlerta)
        self.__estadoActuador = estado
        self.__tipoActuador = tipoActuador
        self.__tipoPuerto = tipoPuerto

    def get_estado_actuador(self):
        """
        @rtype: Char(1)
        @return: Devuelve el estado de un actuador"""
        return self.__estadoActuador

    def get_tipo_actuador(self):
        """
        @rtype: TipoActuador
        @return: Devuelve el tipo de actuador del actuador"""
        return self.__tipoActuador
    
    def get_tipo_puerto(self):
        """
        @rtype: TipoPuerto
        @return: Devuelve el tipo de puerto en el que está conectado el actuador."""
        return self.__tipoPuerto

    def set_estado_actuador(self, value):
        """Asigna un estado al actuador, estos pueden ser: A= Apagado ó E= Encendido"""
        self.__estadoActuador = value

    def set_tipo_actuador(self, value):
        """Asigna un TipoActuador como tipo de actuador del actuador"""
        self.__tipoActuador = value
        
    def set_tipo_puerto(self, value):
        """Asigna un tipoPuerto como el tipo de puerto al que está conectado un actuador"""
        self.__tipoPuerto = value

    estadoActuador = property(get_estado_actuador, set_estado_actuador, None, None)
    tipoActuador = property(get_tipo_actuador, set_tipo_actuador, None, None)
    tipoPuerto = property(get_tipo_puerto, set_tipo_puerto, None, None)
