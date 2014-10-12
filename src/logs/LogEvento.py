# -*- encoding: utf-8 -*-

class LogEvento(object):
    """
    La clase LogEvento se utiliza para contener los atributos que definen un evento que amerita ser notificado y persistido.
    A partir de sus atributos se emitirán notificaciones vía mail o sms.
    """
    
    __idLogEvento= None
    __tipoLog= None
    __dispositivo= None
    __mensaje= None
    __fecha= None

    def __init__(self, idLogEvento, tipoLog, dispositivo, mensaje, fecha):
        """Constructor de la clase LogEvento.
        @type idLogEvento: int
        @param idLogEvento: Identificador del logEvento
        @type tipoLog: TipoLog
        @param tipoLog: Tipo de log al que pertenece el LogEvento
        @type dispositivo: Dispositivo
        @param dispositivo: Dispositivo que genera el log
        @type mensaje: Mensaje
        @param mensaje: Mensaje emitido en el log
        @type fecha: Datetime
        @param fecha: Fecha y hora en el que se genera el LogEvento"""
        self.__idLogEvento = idLogEvento
        self.__tipoLog = tipoLog
        self.__dispositivo = dispositivo
        self.__mensaje = mensaje
        self.__fecha = fecha

    def get_id_log_evento(self):
        """
        @rtype: int
        @return: Devuelve el identificador del LogEvento"""
        return self.__idLogEvento

    def get_tipo_log(self):
        """
        @rtype: TipoLog
        @return: Devuelve el TipoLog al que pertenece el LogEvento"""
        return self.__tipoLog

    def get_dispositivo(self):
        """
        @rtype: Dispositivo
        @return: Devuelve el dispositivo que generó el LogEvento"""
        return self.__dispositivo

    def get_mensaje(self):
        """
        @rtype: Mensaje
        @return: Devuelve el Mensaje a emitir en el LogEvento"""
        return self.__mensaje

    def get_fecha(self):
        """
        @rtype: Datetime
        @return: Devuelve la fecha y hora en la que se generó el LogEvento"""
        return self.__fecha

    def set_id_log_evento(self, value):
        """Asigna un int como identificador del LogEvento"""
        self.__idLogEvento = value

    def set_tipo_log(self, value):
        """Asigna un TipoLog como el tipo de log al que pertenece el LogEvento"""
        self.__tipoLog = value

    def set_dispositivo(self, value):
        """Asigna un Dispositivo como el dispositivo generador del LogEvento"""
        self.__dispositivo = value

    def set_mensaje(self, value):
        """Asigna un Mensaje como el mensaje a ser emitido en el LogEvento"""
        self.__mensaje = value

    def set_fecha(self, value):
        """Asigna un Datetime como la fecha y hora en la que se generó el LogEvento"""
        self.__fecha = value

    idLogEvento = property(get_id_log_evento, set_id_log_evento, None, None)
    tipoLog = property(get_tipo_log, set_tipo_log, None, None)
    dispositivo = property(get_dispositivo, set_dispositivo, None, None)
    mensaje = property(get_mensaje, set_mensaje, None, None)
    fecha = property(get_fecha, set_fecha, None, None)
    