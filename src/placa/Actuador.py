# -*- encoding: utf-8 -*-
from src.placa.Dispositivo import Dispositivo

class Actuador(Dispositivo):
    """
    La clase actuador se utiliza para representar un dispositivo de tipo actuador.
    Además de los atributos de un dispositivo tiene un estadoActuador de tipo Char(1),
     que puede ser E= Encendido ó A= Apagado, y un tipoActuador de tipo tipoActuador,
      por ejemplo, ventilador, y un atributo tipoPuerto que indica 
    si está conectado a un puerto analógico, digital de entrada ó digital de salida
    """
    __estadoActuador= None
    __tipoActuador= None
    __tipoPuerto= None

    def __init__(self, idDispositivo, nombre, modelo, numeroPuerto, activoSistema, padre, estado, tipoActuador, tipoPuerto):
        """
        Constructor de un actuador, recibe como parámetros:
            -idDispositivo : int (dispositivo)
            -nombre: String (dispositivo)
            -modelo: String (dispositivo)
            -numeroPuerto: int (dispositivo)
            -activoSistema: Boolean (dispositivo)
            -estado: Char(1) (actuador)
            -tipoActuador: tipoActuador (actuador)
            -tipoPuerto: tipoPuerto (actuador)
        """
        Dispositivo.__init__(self, 
            idDispositivo, nombre, modelo, numeroPuerto, activoSistema, padre)
        self.__estadoActuador = estado
        self.__tipoActuador = tipoActuador
        self.__tipoPuerto = tipoPuerto

    def get_estado_actuador(self):
        """
        Devuelve el estado de un actuador como un Char(1)
        """
        return self.__estadoActuador


    def get_tipo_actuador(self):
        """
        Devuelve el tipo de actuador como un tipoActuador
        """
        return self.__tipoActuador
    
    def get_tipo_puerto(self):
        """
        Devuelve el tipo de puerto en el que está conectado un actuador como un tipoPuerto
        """
        return self.__tipoPuerto



    def set_estado_actuador(self, value):
        """
        Asigna un estado al actuador, estos pueden ser:
        A= Apagado
        E= Encendido
        """
        self.__estadoActuador = value


    def set_tipo_actuador(self, value):
        """
        Asigna un tipo de actuador al actuador
        """
        self.__tipoActuador = value
        
    def set_tipo_puerto(self, value):
        """
        Asigna un tipoPuerto como el tipo de puerto al que está conectado un actuador
        """
        self.__tipoPuerto = value

    estadoActuador = property(get_estado_actuador, set_estado_actuador, None, None)
    tipoActuador = property(get_tipo_actuador, set_tipo_actuador, None, None)
    tipoPuerto = property(get_tipo_puerto, set_tipo_puerto, None, None)
        
    



    
        