class TipoPuerto(object):
    """
    La clase tipoPuerto es utilizada para instanciar un tipo de puerto al que pueden estar conectados
    un sensor o un actuador. Los posibles tipos de puerto son:
    -analógico
    -entrada digital
    -salida digital
    """
    
    __idTipoPuerto=None
    __nombre=None

    def __init__(self, idTipoPuerto, nombre):
        """
        Constructor de la clase tipoPuerto, recibe como parámetros:
        -idTipoPuerto: int
        -nombre: String (este puede ser: "analogico", "entrada digital" o "salida digital")
        """
        self.__idTipoPuerto= idTipoPuerto
        self.__nombre = nombre

    def get_nombre(self):
        """
        Devuelve el nombre de un tipoPuerto como un String
        """
        return self.__nombre


    def set_nombre(self, value):
        """
        Asigna un String como nombre de un tipoPuerto
        """
        self.__nombre = value

    def get_id_tipo_puerto(self):
        """
        Devuelve el id de un tipoPuerto como un int
        """
        return self.__idTipoPuerto


    def set_id_tipo_puerto(self, value):
        """
        Asigna un int como id de un tipoPuerto
        """
        self.__idTipoPuerto = value

    nombre = property(get_nombre, set_nombre, None, None)
    id = property(get_id_tipo_puerto, set_id_tipo_puerto, None, None)



    
        