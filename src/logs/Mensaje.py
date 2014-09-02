# -*- encoding: utf-8 -*-
class Mensaje(object):
    """
    Clase utilizada para centralizar el manejo de mensajes del sistema.
    Sus atributos son un id de mensaje, un tipo y su texto.
    """
    
    __idMensaje=None
    __tipo=None
    __texto=None

    def __init__(self, idMensaje, tipo, texto):
        """
        Constructor de la clase mensaje, recibe como parámetros:
            -idMensaje : int 
            -tipo: String
            -texto: String
        """
        self.__idMensaje = idMensaje
        self.__tipo = tipo
        self.__texto = texto

    def get_id_mensaje(self):
        """
        Devuelve el id del mensaje como un int
        """
        return self.__idMensaje


    def get_tipo(self):
        """
        Devuelve el tipo del mensaje como un String
        """
        return self.__tipo


    def get_texto(self):
        """
        Devuelve el texto del mensaje como un String
        """
        return self.__texto


    def set_id_mensaje(self, value):
        """
        Asigna un int como id del mensaje
        """
        self.__idMensaje = value


    def set_tipo(self, value):
        """
        Asigna un String como tipo del mensaje
        """
        self.__tipo = value


    def set_texto(self, value):
        """
        Asigna un String como texto del mensaje
        """
        self.__texto = value

    idMensaje = property(get_id_mensaje, set_id_mensaje, None, None)
    tipo = property(get_tipo, set_tipo, None, None)
    texto = property(get_texto, set_texto, None, None)



    
        