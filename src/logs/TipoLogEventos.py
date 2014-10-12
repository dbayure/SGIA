# -*- encoding: utf-8 -*-

class TipoLogEventos(object):
    """
    La clase TipoLogEventos define los tipos de eventos que pueden generarse en el sistema.
    Indican para cada tipo si generan notificaciones por sms y mail y contiene la lista de destinatarios a la que debe notificar ante la generación de un LogEvento de ese TipoLogEvento.
    """
    
    __idTipoLogEvento= None
    __nombre= None
    __enviarSMS= None
    __enviarMAIL= None
    __listaDestinatarios= None

    def __init__(self, idTipoLogEvento, nombre, enviarSMS, enviarMAIL, listaDestinatarios):
        """Constructor de la clase TipoLogEventos.
        @type idTipoLogEvento: int
        @param idTipoLogEvento: Identificador del tipo de log de evento.
        @type nombre: String
        @param nombre: Nombre del tipo de log de evento.
        @type enviarSMS: Char(1)
        @param enviarSMS: Indica si corresponde enviar notificación por SMS (S/N)
        @type enviarMAIL: Char(1)
        @param enviarMAIL: Indica si corresponde enviar notificación por mail (S/N)
        @type listaDestinatarios: List<Destinatarios>
        @param listaDestinatarios: Lista de destinatarios a los que debe enviarse notificaciones de este TipoLogEventos"""
        self.__idTipoLogEvento = idTipoLogEvento
        self.__nombre = nombre
        self.__enviarSMS = enviarSMS
        self.__enviarMAIL = enviarMAIL
        self.__listaDestinatarios = listaDestinatarios

    def get_id_tipo_log_evento(self):
        """
        @rtype: int
        @return: Devuelve el identificador del TipoLogEvento"""
        return self.__idTipoLogEvento

    def get_nombre(self):
        """
        @rtype: String
        @return: Devuelve el nombre del TipoLogEvento"""
        return self.__nombre

    def get_enviar_sms(self):
        """
        @rtype: Char(1)
        @return: Devuelve un char que indica si debe enviarse SMS (S/N)"""
        return self.__enviarSMS

    def get_enviar_mail(self):
        """
        @rtype: Char(1)
        @return: Devuelve un char que indica si debe enviarse mail (S/N)"""
        return self.__enviarMAIL

    def get_lista_destinatarios(self):
        """
        @rtype: List<Destinatario>
        @return: Devuelve la lista de destinatarios a los que se le debe enviar notificaciones."""
        return self.__listaDestinatarios

    def set_id_tipo_log_evento(self, value):
        """Asigna un int como identificador del TipoLogEvento"""
        self.__idTipoLogEvento = value

    def set_nombre(self, value):
        """Asigna un String como nombre del TipoLogEvento"""
        self.__nombre = value

    def set_enviar_sms(self, value):
        """Asigna un Char(1) (S/N) para determinar si corresponde enviar SMS"""
        self.__enviarSMS = value

    def set_enviar_mail(self, value):
        """Asigna un Char(1) (S/N) para determinar si corresponde enviar mail"""
        self.__enviarMAIL = value

    def set_lista_destinatarios(self, value):
        """Asigna una List<Destinatario> como la lista de destinatarios a quienes debe enviarse notificaciones"""
        self.__listaDestinatarios = value

    idTipoLogEvento = property(get_id_tipo_log_evento, set_id_tipo_log_evento, None, None)
    nombre = property(get_nombre, set_nombre, None, None)
    enviarSMS = property(get_enviar_sms, set_enviar_sms, None, None)
    enviarMAIL = property(get_enviar_mail, set_enviar_mail, None, None)
    listaDestinatarios = property(get_lista_destinatarios, set_lista_destinatarios, None, None)
