# -*- encoding: utf-8 -*-
class TipoPlaca(object):
    """
    La clase tipoPlaca es utilizada para instanciar un tipo de placa que categoriza a una placa auxiliar. 
    Algunos de los posibles tipos de placa pueden ser:
    -placa de reles
    -placa de extension USB
    """
    
    __idTipoPlaca=None
    __nombre=None

    def __init__(self, idTipoPlaca, nombre):
        """
        Constructor de la clase tipoPlaca, recibe como parámetros:
        -idTipoPlaca: int
        -nombre: String (este puede ser: "analogico", "entrada digital" o "salida digital")
        """
        self.__idTipoPlaca= idTipoPlaca
        self.__nombre = nombre

    def get_nombre(self):
        """
        Devuelve el nombre de un tipoPlaca como un String
        """
        return self.__nombre


    def set_nombre(self, value):
        """
        Asigna un String como nombre de un tipoPlaca
        """
        self.__nombre = value

    def get_id_tipo_placa(self):
        """
        Devuelve el id de un tipoPlaca como un int
        """
        return self.__idTipoPlaca


    def set_id_tipo_placa(self, value):
        """
        Asigna un int como id de un tipoPlaca
        """
        self.__idTipoPlaca = value

    nombre = property(get_nombre, set_nombre, None, None)
    id = property(get_id_tipo_placa, set_id_tipo_placa, None, None)



    
        