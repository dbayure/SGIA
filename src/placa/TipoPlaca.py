# -*- encoding: utf-8 -*-
class TipoPlaca(object):
    """
    La clase tipoPlaca es utilizada para instanciar un tipo de placa que categoriza a una placa auxiliar. 
    Algunos de los posibles tipos de placa pueden ser: placa de reles, placa de extension USB, etc.
    """
    
    __idTipoPlaca=None
    __nombre=None

    def __init__(self, idTipoPlaca, nombre):
        """
        Constructor de la clase tipoPlaca.
        @type idTipoPlaca: int
        @param idTipoPlaca: Identificador de tipo placa
        @type nombre: String
        @param nombre: Nombre del tipo de placa"""
        self.__idTipoPlaca= idTipoPlaca
        self.__nombre = nombre

    def get_nombre(self):
        """
        @rtype: String
        @return: Devuelve el nombre de un TipoPlaca"""
        return self.__nombre

    def set_nombre(self, value):
        """Asigna un String como nombre del TipoPlaca"""
        self.__nombre = value

    def get_id_tipo_placa(self):
        """
        @rtype: int
        @return: Devuelve el identificador de un tipoPlaca"""
        return self.__idTipoPlaca

    def set_id_tipo_placa(self, value):
        """Asigna un int como identificador de un TipoPlaca"""
        self.__idTipoPlaca = value

    nombre = property(get_nombre, set_nombre, None, None)
    id = property(get_id_tipo_placa, set_id_tipo_placa, None, None)
