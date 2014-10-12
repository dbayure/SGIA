# -*- encoding: utf-8 -*-
class TipoActuador(object):
    """
    La clase tipoActuador es utilizada para instanciar un tipo de actuador, estos pueden ser, por ejemplo, ventiladores, aspersores, cortinas, etc.
    Sus atributos son idTipoActuador y categoría.
    """

    __idTipoActuador= None
    __categoria=None
    
    def __init__(self, idTipoActuador, categoria):
        """
        Constructor de la clase tipoActuador
        @type idTipoActuador: int
        @param idTipoActuador: Identificador del tipo de actuador.
        @type categoria: String
        @param categoria: Categoría del tipo actuador, estas pueden ser, por ejemplo, "ventilador", "aspersor", "cortina", etc."""
        self.__idTipoActuador = idTipoActuador
        self.__categoria = categoria

    def get_id_tipo_actuador(self):
        """
        @rtype: int
        @return: Devuelve el identificador del tipoActuador."""
        return self.__idTipoActuador

    def get_categoria(self):
        """
        @rtype: String
        @return: Devuelve la categoria del tipoActuador."""
        return self.__categoria

    def set_id_tipo_actuador(self, value):
        """Asigna un int como identificador del tipoActuador"""
        self.__idTipoActuador = value

    def set_categoria(self, value):
        """Asigna un String como categoria del tipoActuador."""
        self.__categoria = value

    idTipoActuador = property(get_id_tipo_actuador, set_id_tipo_actuador, None, None)
    categoria = property(get_categoria, set_categoria, None, None)
