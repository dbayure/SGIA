# -*- encoding: utf-8 -*-

class DatosPlaca(object):
    """
    Clase utilizada para contener los datos de una placa, y posteriormente pasarlo por WS a la centralizadora.
    """
    
    
    __nroSeriePlaca=None
    __estadoPlaca=None
    __hostWS_SMS=None
    __puertoWS_SMS= None
    __hostWS_Centralizadora= None
    __puertoWS_Centralizadora= None
    __periodicidadLecturas= None
    __periodicidadNiveles= None
    __estadoAlerta= None

    def __init__(self, nroSeriePlaca, estadoPlaca, hostWS_SMS, puertoWS_SMS, hostWS_Centralizadora, puertoWS_Centralizadora, periodicidadLecturas, periodicidadNiveles, estadoAlerta):
        self.__nroSeriePlaca = nroSeriePlaca
        self.__estadoPlaca = estadoPlaca
        self.__hostWS_SMS = hostWS_SMS
        self.__puertoWS_SMS = puertoWS_SMS
        self.__hostWS_Centralizadora = hostWS_Centralizadora
        self.__puertoWS_Centralizadora = puertoWS_Centralizadora
        self.__periodicidadLecturas = periodicidadLecturas
        self.__periodicidadNiveles = periodicidadNiveles
        self.__estadoAlerta = estadoAlerta

    def get_nro_serie_placa(self):
        return self.__nroSeriePlaca


    def get_estado_placa(self):
        return self.__estadoPlaca

    def get_host_ws_sms(self):
        return self.__hostWS_SMS


    def get_puerto_ws_sms(self):
        return self.__puertoWS_SMS


    def get_host_ws_centralizadora(self):
        return self.__hostWS_Centralizadora


    def get_puerto_ws_centralizadora(self):
        return self.__puertoWS_Centralizadora


    def get_periodicidad_lecturas(self):
        return self.__periodicidadLecturas


    def get_periodicidad_niveles(self):
        return self.__periodicidadNiveles


    def get_estado_alerta(self):
        return self.__estadoAlerta


    def set_nro_serie_placa(self, value):
        self.__nroSeriePlaca = value


    def set_estado_placa(self, value):
        self.__estadoPlaca = value


    def set_host_ws_sms(self, value):
        self.__hostWS_SMS = value


    def set_puerto_ws_sms(self, value):
        self.__puertoWS_SMS = value


    def set_host_ws_centralizadora(self, value):
        self.__hostWS_Centralizadora = value


    def set_puerto_ws_centralizadora(self, value):
        self.__puertoWS_Centralizadora = value


    def set_periodicidad_lecturas(self, value):
        self.__periodicidadLecturas = value


    def set_periodicidad_niveles(self, value):
        self.__periodicidadNiveles = value

    def set_estado_alerta(self, value):
        self.__estadoAlerta = value
