class Resultado(object):
    """
    La clase resultado se utiliza para instanciar resultados de lecturas o acciones disparadas.
    De esta heredan las clases ResultadoAccion y ResultadoLectura.
    Tiene como atributos un mensaje y la fecha en la que se obtiene.
    """
    
    __mensaje=None
    __fecha=None

    def __init__(self, mensaje, fecha):
        """
        Constructor de la clase Resultado, recibe como parámetros:
            -mensaje: Mensaje
            -fecha: Date
        """
        self.__mensaje = mensaje
        self.__fecha= fecha

    def get_mensaje(self):
        """
        Devuelve el mensaje de un resultado como un Mensaje
        """
        return self.__mensaje
    
    def get_fecha(self):
        """
        Devuelve la fecha de un resultado como un Date
        """
        return self.__fecha


    def set_mensaje(self, value):
        """
        Asigna un Mensaje como mensaje de un resultado
        """
        self.__mensaje = value
        
    def set_fecha(self, value):
        """
        Asigna un Date como fecha de un resultado
        """
        self.__fecha = value

    mensaje = property(get_mensaje, set_mensaje, None, None)
    fecha = property(get_fecha, set_fecha, None, None)


    
        