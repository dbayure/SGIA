# -*- encoding: utf-8 -*-
from Phidgets.Devices.InterfaceKit import InterfaceKit
class Herramientas(object):
    """
    Clase con métodos auxiliares que sirven de apoyo a otros procedimientos del sistema
    """
    
    __ipWS= None
    __puertoWS= None

    def __init__(self):
        self.__ipWS= '192.168.0.102'
        self.__puertoWS= 5001
        
    def instanciarIK (self, nroSerie):
        """
        Método utilizado para instanciar un objeto de tipo InterfaceKit de la API de Phidgets, que permite interactuar con 
        la placa controladora y sus puertos"""
        ik= InterfaceKit()
        ik.openRemoteIP(self.__ipWS, self.__puertoWS, nroSerie)
        ik.waitForAttach(10000)
        return ik