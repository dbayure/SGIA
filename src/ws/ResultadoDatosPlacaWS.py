# -*- encoding: utf-8 -*-
from soaplib.serializers.clazz import ClassSerializer
from soaplib.serializers.primitive import DateTime, Integer, String
from src.logs.Mensaje import Mensaje

class ResultadoDatosPlacaWS(ClassSerializer):
    """
    Clase utilizada para convertir a un objeto serializable un resultado lectura para enviarlo en respuesta a una llamada de web service
    """
    class types:
        nroSeriePlaca=String
        estadoPlaca=String
        hostWS_SMS=String
        puertoWS_SMS=String
        hostWS_Centralizadora= String
        puertoWS_Centralizadora= String
        periodicidadLecturas= Integer
        periodicidadNiveles= Integer
        estadoAlerta= String

    def __init__(self, nroSeriePlaca, estadoPlaca, hostWS_SMS, puertoWS_SMS, hostWS_Centralizadora, puertoWS_Centralizadora, periodicidadLecturas, periodicidadNiveles, estadoAlerta):
        self.nroSeriePlaca = nroSeriePlaca
        self.estadoPlaca = estadoPlaca
        self.hostWS_SMS = hostWS_SMS
        self.puertoWS_SMS = puertoWS_SMS
        self.hostWS_Centralizadora = hostWS_Centralizadora
        self.puertoWS_Centralizadora = puertoWS_Centralizadora
        self.periodicidadLecturas = periodicidadLecturas
        self.periodicidadNiveles = periodicidadNiveles
        self.estadoAlerta = estadoAlerta

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


    def del_nro_serie_placa(self):
        del self.__nroSeriePlaca


    def del_estado_placa(self):
        del self.__estadoPlaca


    def del_host_ws_sms(self):
        del self.__hostWS_SMS


    def del_puerto_ws_sms(self):
        del self.__puertoWS_SMS


    def del_host_ws_centralizadora(self):
        del self.__hostWS_Centralizadora


    def del_puerto_ws_centralizadora(self):
        del self.__puertoWS_Centralizadora


    def del_periodicidad_lecturas(self):
        del self.__periodicidadLecturas


    def del_periodicidad_niveles(self):
        del self.__periodicidadNiveles


    def del_estado_alerta(self):
        del self.__estadoAlerta

    nroSeriePlaca = property(get_nro_serie_placa, set_nro_serie_placa, del_nro_serie_placa, "nroSeriePlaca's docstring")
    estadoPlaca = property(get_estado_placa, set_estado_placa, del_estado_placa, "estadoPlaca's docstring")
    hostWS_SMS = property(get_host_ws_sms, set_host_ws_sms, del_host_ws_sms, "hostWS_SMS's docstring")
    puertoWS_SMS = property(get_puerto_ws_sms, set_puerto_ws_sms, del_puerto_ws_sms, "puertoWS_SMS's docstring")
    hostWS_Centralizadora = property(get_host_ws_centralizadora, set_host_ws_centralizadora, del_host_ws_centralizadora, "hostWS_Centralizadora's docstring")
    puertoWS_Centralizadora = property(get_puerto_ws_centralizadora, set_puerto_ws_centralizadora, del_puerto_ws_centralizadora, "puertoWS_Centralizadora's docstring")
    periodicidadLecturas = property(get_periodicidad_lecturas, set_periodicidad_lecturas, del_periodicidad_lecturas, "periodicidadLecturas's docstring")
    periodicidadNiveles = property(get_periodicidad_niveles, set_periodicidad_niveles, del_periodicidad_niveles, "periodicidadNiveles's docstring")
    estadoAlerta = property(get_estado_alerta, set_estado_alerta, del_estado_alerta, "estadoAlerta's docstring")



    
