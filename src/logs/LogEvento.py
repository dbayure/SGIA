# -*- encoding: utf-8 -*-

class LogEvento(object):
    """
    La clase logEventos se utiliza para contener los atributos que definen un evento que amerita ser notificado y persistido.
    A partir de sus atributos se emitirán notificaciones vía mail o sms
    """
    
    __idLogEvento= None
    __tipoLog= None
    __dispositivo= None
    __mensaje= None
    __fecha= None

    def __init__(self, idLogEvento, tipoLog, dispositivo, mensaje, fecha):
        self.__idLogEvento = idLogEvento
        self.__tipoLog = tipoLog
        self.__dispositivo = dispositivo
        self.__mensaje = mensaje
        self.__fecha = fecha

    def get_id_log_evento(self):
        return self.__idLogEvento


    def get_tipo_log(self):
        return self.__tipoLog


    def get_dispositivo(self):
        return self.__dispositivo


    def get_mensaje(self):
        return self.__mensaje


    def get_fecha(self):
        return self.__fecha


    def set_id_log_evento(self, value):
        self.__idLogEvento = value


    def set_tipo_log(self, value):
        self.__tipoLog = value


    def set_dispositivo(self, value):
        self.__dispositivo = value


    def set_mensaje(self, value):
        self.__mensaje = value


    def set_fecha(self, value):
        self.__fecha = value

    idLogEvento = property(get_id_log_evento, set_id_log_evento, None, None)
    tipoLog = property(get_tipo_log, set_tipo_log, None, None)
    dispositivo = property(get_dispositivo, set_dispositivo, None, None)
    mensaje = property(get_mensaje, set_mensaje, None, None)
    fecha = property(get_fecha, set_fecha, None, None)
    