# -*- encoding: utf-8 -*-
from soaplib.serializers.clazz import ClassSerializer
from soaplib.serializers.primitive import String, Integer

class Mensaje(ClassSerializer):
    """
    Clase utilizada para centralizar el manejo de mensajes del sistema.
    Sus atributos son un id de mensaje, un tipo y su texto.
    """
    #__type_name__='Mensaje'
    class types:
        idMensaje=Integer
        tipo=String
        texto=String

    def __init__(self, idMensaje, tipo, texto):
        """
        Constructor de la clase mensaje, recibe como parámetros:
            -idMensaje : int 
            -tipo: String
            -texto: String
        """
        self.idMensaje = idMensaje
        self.tipo = tipo
        self.texto = texto

    def get_id_mensaje(self):
        """
        Devuelve el id del mensaje como un int
        """
        return self.idMensaje


    def get_tipo(self):
        """
        Devuelve el tipo del mensaje como un String
        """
        return self.tipo


    def get_texto(self):
        """
        Devuelve el texto del mensaje como un String
        """
        return self.texto


    def set_id_mensaje(self, value):
        """
        Asigna un int como id del mensaje
        """
        self.idMensaje = value


    def set_tipo(self, value):
        """
        Asigna un String como tipo del mensaje
        """
        self.tipo = value


    def set_texto(self, value):
        """
        Asigna un String como texto del mensaje
        """
        self.texto = value

    #idMensaje = property(get_id_mensaje, set_id_mensaje, None, None)
    #tipo = property(get_tipo, set_tipo, None, None)
    #texto = property(get_texto, set_texto, None, None)
    
    



    
        