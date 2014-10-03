# -*- encoding: utf-8 -*-

class Destinatario(object):
    """
    La clase destinatario tiene los atributos que determinan las condiciones para envío de notificaciones, tales como el celular y mail de destino
    y los horarios en los que admite notificaciones.
    """
    
    __idDestinatario= None
    __nombre= None
    __celular= None
    __mail= None
    __horaMin= None
    __horaMax= None

    def __init__(self, idDestinatario, nombre, celular, mail, horaMin, horaMax):
        self.__idDestinatario = idDestinatario
        self.__nombre = nombre
        self.__celular = celular
        self.__mail = mail
        self.__horaMin = horaMin
        self.__horaMax = horaMax

    def get_id_destinatario(self):
        return self.__idDestinatario


    def get_nombre(self):
        return self.__nombre


    def get_celular(self):
        return self.__celular


    def get_mail(self):
        return self.__mail


    def get_hora_min(self):
        return self.__horaMin


    def get_hora_max(self):
        return self.__horaMax


    def set_id_destinatario(self, value):
        self.__idDestinatario = value


    def set_nombre(self, value):
        self.__nombre = value


    def set_celular(self, value):
        self.__celular = value


    def set_mail(self, value):
        self.__mail = value


    def set_hora_min(self, value):
        self.__horaMin = value


    def set_hora_max(self, value):
        self.__horaMax = value

    idDestinatario = property(get_id_destinatario, set_id_destinatario, None, None)
    nombre = property(get_nombre, set_nombre, None, None)
    celular = property(get_celular, set_celular, None, None)
    mail = property(get_mail, set_mail, None, None)
    horaMin = property(get_hora_min, set_hora_min, None, None)
    horaMax = property(get_hora_max, set_hora_max, None, None)
