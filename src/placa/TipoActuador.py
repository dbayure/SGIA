# -*- encoding: utf-8 -*-
class TipoActuador(object):
    """
    La clase tipoActuador es utilizada para instanciar un tipo de actuador, estos pueden ser,
    por ejemplo, ventiladores, aspersores, cortinas, etc.
    Sus atributos son idTipoActuador y categoría.
    """

    __idTipoActuador= None
    __categoria=None
    
    def __init__(self, idTipoActuador, categoria):
        """
        Constructor de la clase tipoActuador, recibe como parámetros:
        -idTipoActuador: int
        -categoria: String (este puede ser por ejemplo: "ventilador", "aspersor", "cortina", etc)
        """
        self.__idTipoActuador = idTipoActuador
        self.__categoria = categoria

    def get_id_tipo_actuador(self):
        """
        Devuelve el id de un tipoActuador como un int
        """
        return self.__idTipoActuador


    def get_categoria(self):
        """
        Devuelve la categoria de un tipoActuador como un String
        """
        return self.__categoria


    def set_id_tipo_actuador(self, value):
        """
        Asigna un int como id de un tipoActuador
        """
        self.__idTipoActuador = value


    def set_categoria(self, value):
        """
        Asigna un String como categoria de un tipoActuador
        """
        self.__categoria = value

    idTipoActuador = property(get_id_tipo_actuador, set_id_tipo_actuador, None, None)
    categoria = property(get_categoria, set_categoria, None, None)

    

    
        