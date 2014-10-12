# -*- encoding: utf-8 -*-
from src.placa.Dispositivo import Dispositivo
from Phidgets.PhidgetException import PhidgetException

class PlacaAuxiliar(Dispositivo):
    """
    La clase placaAuxiliar se utiliza para representar un dispositivo "Interface Kit".
    Estos son los que se conectan directamente a la placa en los puertos USB, como por ejemplo, una placa de relés, o una extensión con puertos analógicos adicionales.
    Además de los atributos de un dispositivo tiene como atributos su número de serie, el tipo de placa auxiliar (por ejemplo, placa de relés), y la lista de dispositivos que están conectados directamente a ella.
    """
    __nroSerie= None
    __tipo= None
    __listaDispositivos= None
    __ik = None
    
    def __init__(self, idDispositivo, nombre, modelo, numeroPuerto, activoSistema, padre, estadoAlerta, nroSerie, tipo, listaDispositivos):
        """
        Constructor de una placaAuxiliar.
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
        @type nroSerie: int
        @param nroSerie: Número de serie de la placa auxiliar.
        @type tipo: TipoPlaca
        @param tipo: Tipo de placa auxiliar
        @type listaDispositivos: List<Dispositivo>
        @param listaDispositivos: Lista de dispositivos conectados directamente a la placa auxiliar."""
        Dispositivo.__init__(self, idDispositivo, nombre, modelo, numeroPuerto, activoSistema, padre, estadoAlerta)
        self.__nroSerie = nroSerie
        self.__tipo = tipo
        self.__listaDispositivos = listaDispositivos
        
    def get_nro_serie(self):
        """
        @rtype: String
        @return: Devuelve el número de serie de una placa auxiliar."""
        return self.__nroSerie

    def get_tipo(self):
        """
        @rtype: TipoPlaca
        @return: Devuelve el tipo de la placa auxiliar."""
        return self.__tipo

    def get_lista_dispositivos(self):
        """
        @rtype: List<Dispositivo>
        @return: Devuelve la lista de dispositivos conectados directamente a una placa auxiliar."""
        return self.__listaDispositivos
    
    def get_ik(self):
        """
        @rtype: InterfaceKit
        @return: Devuelve el interface kit de la placa auxiliar."""
        return self.__ik

    def set_nro_serie(self, value):
        """Asigna un String como número de serie de la placa auxiliar"""
        self.__nroSerie = value

    def set_tipo(self, value):
        """Asigna un String como tipo de placa de la placa auxiliar."""
        self.__tipo = value

    def set_lista_dispositivos(self, value):
        """Asigna una List<Dispositivo> como la lista de dispositivos de la placa auxiliar."""
        self.__listaDispositivos = value
        
    def set_ik(self, value):
        """Asigna un InterfaceKit a la placa auxiliar."""
        self.__ik = value
        
    def cerrarIK(self):
        """Método para cerrar la conexión al interface kit instanciado por la placa auxiliar."""
        try:
            self.ik.closePhidget()
        except PhidgetException as e:
            print("Phidget Exception %i: %s" % (e.code, e.details))
            print("Exiting....4")
            
    def __del__(self):
        """Método invocado automáticamente al destruir una instancia de la clase, se asegura que se cierre la conexión al interface kit instanciado"""
        if self.__ik <> None:
            self.cerrarIK() 

    nroSerie = property(get_nro_serie, set_nro_serie, None, None)
    tipo = property(get_tipo, set_tipo, None, None)
    listaDispositivos = property(get_lista_dispositivos, set_lista_dispositivos, None, None)
    ik = property(get_ik, set_ik, None, None)
