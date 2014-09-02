# -*- encoding: utf-8 -*-
from src.placa.Dispositivo import Dispositivo

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
    
    def __init__(self, idDispositivo, nombre, modelo, numeroPuerto, activoSistema, nroSerie, tipo, listaDispositivos):
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
        Dispositivo.__init__(self, 
            idDispositivo, nombre, modelo, numeroPuerto, activoSistema)
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

    nroSerie = property(get_nro_serie, set_nro_serie, None, None)
    tipo = property(get_tipo, set_tipo, None, None)
    listaDispositivos = property(get_lista_dispositivos, set_lista_dispositivos, None, None)
            


    
        