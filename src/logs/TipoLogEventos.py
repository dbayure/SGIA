# -*- encoding: utf-8 -*-

class TipoLogEventos(object):
    """
    La clase TipoLogEventos define los tipos de eventos que pueden generarse en el sistema.
    Indican para cada tipo si generan notificaciones por sms y mail y contiene la lista de destinatarios a la que debe enviarse.
    """
    
    __idTipoLogEvento= None
    __nombre= None
    __enviarSMS= None
    __enviarMAIL= None
    __listaDestinatarios= None

    def __init__(self, idTipoLogEvento, nombre, enviarSMS, enviarMAIL, listaDestinatarios):
        self.__idTipoLogEvento = idTipoLogEvento
        self.__nombre = nombre
        self.__enviarSMS = enviarSMS
        self.__enviarMAIL = enviarMAIL
        self.__listaDestinatarios = listaDestinatarios

    def get_id_tipo_log_evento(self):
        return self.__idTipoLogEvento


    def get_nombre(self):
        return self.__nombre


    def get_enviar_sms(self):
        return self.__enviarSMS


    def get_enviar_mail(self):
        return self.__enviarMAIL


    def get_lista_destinatarios(self):
        return self.__listaDestinatarios


    def set_id_tipo_log_evento(self, value):
        self.__idTipoLogEvento = value


    def set_nombre(self, value):
        self.__nombre = value


    def set_enviar_sms(self, value):
        self.__enviarSMS = value


    def set_enviar_mail(self, value):
        self.__enviarMAIL = value


    def set_lista_destinatarios(self, value):
        self.__listaDestinatarios = value

    idTipoLogEvento = property(get_id_tipo_log_evento, set_id_tipo_log_evento, None, None)
    nombre = property(get_nombre, set_nombre, None, None)
    enviarSMS = property(get_enviar_sms, set_enviar_sms, None, None)
    enviarMAIL = property(get_enviar_mail, set_enviar_mail, None, None)
    listaDestinatarios = property(get_lista_destinatarios, set_lista_destinatarios, None, None)


    