# -*- encoding: utf-8 -*-
from src.placa.Dispositivo import Dispositivo

class ActuadorAvance(Dispositivo):
    """
    La clase ActuadorAvance se utiliza para representar un dispositivo de tipo actuador de avance.
    Además de los atributos de un dispositivo tiene una posición que determina en que estado de avance
    está el actuador, puede tener un estado de retroceso y un puerto asociado para lograr este efecto, 
    un tipoActuador de tipo tipoActuador, por ejemplo, cortinas, un atributo tipoPuerto que indica 
    si está conectado a un puerto analógico, digital de entrada ó digital de salida y un tiempo de tolerancia 
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
        Dispositivo.__init__(self, 
            idDispositivo, nombre, modelo, numeroPuerto, activoSistema, padre, estadoAlerta)
        self.__posicion = posicion
        self.__tipoActuador = tipoActuador
        self.__tipoPuerto = tipoPuerto
        self.__numeroPuertoRetroceso = numeroPuertoRetroceso
        self.__tipoPuertoRetroceso = tipoPuertoRetroceso
        self.__tiempoEntrePosiciones = tiempoEntrePosiciones
        self.__listaPosiciones = listaPosiciones

    def get_posicion(self):
        return self.__posicion

    def get_tipo_actuador(self):
        return self.__tipoActuador

    def get_tipo_puerto(self):
        return self.__tipoPuerto

    def get_numero_puerto_retroceso(self):
        return self.__numeroPuertoRetroceso

    def get_tipo_puerto_retroceso(self):
        return self.__tipoPuertoRetroceso

    def get_tiempo_entre_posiciones(self):
        return self.__tiempoEntrePosiciones

    def get_lista_posiciones(self):
        return self.__listaPosiciones

    def set_posicion(self, value):
        self.__posicion = value

    def set_tipo_actuador(self, value):
        self.__tipoActuador = value

    def set_tipo_puerto(self, value):
        self.__tipoPuerto = value

    def set_numero_puerto_retroceso(self, value):
        self.__numeroPuertoRetroceso = value

    def set_tipo_puerto_retroceso(self, value):
        self.__tipoPuertoRetroceso = value

    def set_tiempo_entre_posiciones(self, value):
        self.__tiempoEntrePosiciones = value

    def set_lista_posiciones(self, value):
        self.__listaPosiciones = value

    posicion = property(get_posicion, set_posicion, None, None)
    tipoActuador = property(get_tipo_actuador, set_tipo_actuador, None, None)
    tipoPuerto = property(get_tipo_puerto, set_tipo_puerto, None, None)
    numeroPuertoRetroceso = property(get_numero_puerto_retroceso, set_numero_puerto_retroceso, None, None)
    tipoPuertoRetroceso = property(get_tipo_puerto_retroceso, set_tipo_puerto_retroceso, None, None)
    tiempoEntrePosiciones = property(get_tiempo_entre_posiciones, set_tiempo_entre_posiciones, None, None)
    listaPosiciones = property(get_lista_posiciones, set_lista_posiciones, None, None)

    
   

    

    
        
    



    
        