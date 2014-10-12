# -*- encoding: utf-8 -*-
class TipoPuerto(object):
    """
    La clase tipoPuerto es utilizada para instanciar un tipo de puerto al que pueden estar conectados un sensor, actuador ó actuador de avance.
    Los posibles tipos de puerto son: analógico,entrada digital, ó salida digital.
    """
    __idTipoPuerto=None
    __nombre=None

    def __init__(self, idTipoPuerto, nombre):
        """
        Constructor de la clase TipoPuerto
        @type idTipoPuerto: int
        @param idTipoPuerto: Identificador de un TipoPuerto
        @type nombre: String
        @param nombre: Nombre de un TipoPuerto, estos pueden ser "analogico", "e-digital" ó "s-digital")"""
        self.__idTipoPuerto= idTipoPuerto
        self.__nombre = nombre

    def get_nombre(self):
        """
        @rtype: String
        @return: Devuelve el nombre de un TipoPuerto"""
        return self.__nombre

    def set_nombre(self, value):
        """Asigna un String como nombre del TipoPuerto"""
        self.__nombre = value

    def get_id_tipo_puerto(self):
        """
        @rtype: int
        @return: Devuelve el identificador de un TipoPuerto"""
        return self.__idTipoPuerto

    def set_id_tipo_puerto(self, value):
        """Asigna un int como identificador de un TipoPuerto"""
        self.__idTipoPuerto = value

    nombre = property(get_nombre, set_nombre, None, None)
    id = property(get_id_tipo_puerto, set_id_tipo_puerto, None, None)
