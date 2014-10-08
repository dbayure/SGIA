# -*- encoding: utf-8 -*-
from src.placa.Dispositivo import Dispositivo
from Phidgets.PhidgetException import PhidgetException
from src.recursos.Herramientas import Herramientas

class PlacaAuxiliar(Dispositivo):
    """
    La clase placaAuxiliar se utiliza para representar un dispositivo "Interface Kit".
    Estos son los que se conectan directamente a la placa en los puertos USB, como por ejemplo,
    una placa de relés, o una extensión con puertos analógicos adicionales.
    Además de los atributos de un dispositivo tiene como atributos su número de serie, el tipo de
    placa auxiliar que es (por ejemplo, placa de relés), y la lista de dispositivos que
    están conectados directamente a ella.
    """

    __nroSerie= None
    __tipo= None
    __listaDispositivos= None
    __ik = None
    
    def __init__(self, idDispositivo, nombre, modelo, numeroPuerto, activoSistema, padre, estadoAlerta, nroSerie, tipo, listaDispositivos):
        """
        Constructor de una placaAuxiliar, recibe como parámetros:
            -idDispositivo : int (dispositivo)
            -nombre: String (dispositivo)
            -modelo: String (dispositivo)
            -numeroPuerto: String (dispositivo)
            -activoSistema: Boolean (dispositivo)
            -nroSerie: int (placaAuxiliar)
            -tipo: String (placaAuxiliar)
            -listaDispositivos: List<dispositivo> (placaAuxiliar)
        """
        Dispositivo.__init__(self, idDispositivo, nombre, modelo, numeroPuerto, activoSistema, padre, estadoAlerta)
        self.__nroSerie = nroSerie
        self.__tipo = tipo
        self.__listaDispositivos = listaDispositivos
        

    def get_nro_serie(self):
        """
        Devuelve el número de serie de una placa auxiliar como un String
        """
        return self.__nroSerie


    def get_tipo(self):
        """
        Devuelve el tipo de una placa auxiliar como un String
        """
        return self.__tipo


    def get_lista_dispositivos(self):
        """
        Devuelve la lista de dispositivos conectados a una placa auxiliar como una List<dispositivo>
        """
        return self.__listaDispositivos
    
    def get_ik(self):
        """
        Devuelve el interface kit de una placa auxiliar
        """
        return self.__ik


    def set_nro_serie(self, value):
        """
        Asigna un String como número de serie de una placa auxiliar
        """
        self.__nroSerie = value


    def set_tipo(self, value):
        """
        Asigna un String como tipo de una placa auxiliar
        """
        self.__tipo = value


    def set_lista_dispositivos(self, value):
        """
        Asigna una List<dispositivo> como la lista de dispositivos de una placa auxiliar
        """
        self.__listaDispositivos = value
        
    def set_ik(self, value):
        """
        Asigna un interface kit a una placa auxiliar
        """
        self.__ik = value
        
    def cerrarIK(self):
        try:
            self.ik.closePhidget()
        except PhidgetException as e:
            print("Phidget Exception %i: %s" % (e.code, e.details))
            print("Exiting....4")
            
    def __del__(self):
        if self.__ik <> None:
            self.cerrarIK() 

    nroSerie = property(get_nro_serie, set_nro_serie, None, None)
    tipo = property(get_tipo, set_tipo, None, None)
    listaDispositivos = property(get_lista_dispositivos, set_lista_dispositivos, None, None)
    ik = property(get_ik, set_ik, None, None)
            


    
        