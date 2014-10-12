# -*- encoding: utf-8 -*-

class Destinatario(object):
    """
    La clase destinatario tiene los atributos que determinan las condiciones para envío de notificaciones, tales como el celular, mail de destino
    y los horarios en los que admite notificaciones.
    """
    
    __idDestinatario= None
    __nombre= None
    __celular= None
    __mail= None
    __horaMin= None
    __horaMax= None

    def __init__(self, idDestinatario, nombre, celular, mail, horaMin, horaMax):
        """Constructor de la clase Destinatario.
        @type idDestinatario: int
        @param idDestinatario: Identificador del destinatario
        @type nombre: String
        @param nombre: Nombre del destinatario
        @type celular: String
        @param celular: Numero de celular para enviar SMS
        @type mail: String
        @param mail: Casilla de mail para envío de notificaciones.
        @type horaMin: int
        @param horaMin: Límite inferior para determinar el rango horario en el que se admiten notificaciones
        @type horaMax: int
        @param horaMax: Límite superior para determinar el rango horario en el que se admiten notificaciones"""
        self.__idDestinatario= idDestinatario
        self.__nombre= nombre
        self.__celular= celular
        self.__mail= mail
        self.__horaMin= horaMin
        self.__horaMax = horaMax

    def get_id_destinatario(self):
        """
        @rtype: int
        @return: Devuelve el id del destinatario"""
        return self.__idDestinatario

    def get_nombre(self):
        """
        @rtype: String
        @return: Devuelve el nombre del destinatario"""
        return self.__nombre

    def get_celular(self):
        """
        @rtype: String
        @return: Devuelve el celular del destinatario"""
        return self.__celular

    def get_mail(self):
        """
        @rtype: String
        @return: Devuelve el mail del destinatario"""
        return self.__mail

    def get_hora_min(self):
        """
        @rtype: int
        @return: Devuelve la horaMin del rango horario permitido para notificaciones"""
        return self.__horaMin

    def get_hora_max(self):
        """
        @rtype: int
        @return: Devuelve la horaMax del rango horario permitido para notificaciones"""
        return self.__horaMax

    def set_id_destinatario(self, value):
        """Asigna un int como idDestinatario del destinatario"""
        self.__idDestinatario = value

    def set_nombre(self, value):
        """Asigna un String como nombre del destinatario."""
        self.__nombre = value

    def set_celular(self, value):
        """Asigna un String como celular del destinatario."""
        self.__celular = value

    def set_mail(self, value):
        """Asigna un String como mail del destinatario."""
        self.__mail = value

    def set_hora_min(self, value):
        """Asigna un int como horaMin para el rango horario permitido del destinatario."""
        self.__horaMin = value

    def set_hora_max(self, value):
        """Asigna un int como horaMax para el rango horario permitido del destinatario."""
        self.__horaMax = value

    idDestinatario = property(get_id_destinatario, set_id_destinatario, None, None)
    nombre = property(get_nombre, set_nombre, None, None)
    celular = property(get_celular, set_celular, None, None)
    mail = property(get_mail, set_mail, None, None)
    horaMin = property(get_hora_min, set_hora_min, None, None)
    horaMax = property(get_hora_max, set_hora_max, None, None)
