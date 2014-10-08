# -*- encoding: utf-8 -*-
class Resultado(object):
    """
    La clase resultado se utiliza para instanciar resultados de lecturas o acciones disparadas.
    De esta heredan las clases ResultadoAccion y ResultadoLectura.
    Tiene como atributos un mensaje y la fecha en la que se obtiene.
    """
    
    __mensaje=None
    __fecha=None

    def __init__(self, mensaje, fecha):
        """Constructor de la clase Resultado
            @type mensaje: Mensaje
            @param mensaje: Mensaje asociado al resultado. 
            @type fecha: Datetime
            @param fecha: Fecha y hora en que se crea el resultado. 
        """
        self.__mensaje = mensaje
        self.__fecha= fecha

    def get_mensaje(self):
        """
        @rtype: Mensaje
        @return: Devuelve el mensaje de un resultado como un Mensaje"""
        return self.__mensaje
    
    def get_fecha(self):
        """
        @rtype: Datetime
        @return: Devuelve la fecha de un resultado como un Datetime"""
        return self.__fecha

    def set_mensaje(self, value):
        """Asigna un Mensaje como mensaje de un resultado"""
        self.__mensaje = value
        
    def set_fecha(self, value):
        """Asigna un Datetime como fecha de un resultado"""
        self.__fecha = value

    mensaje = property(get_mensaje, set_mensaje, None, None)
    fecha = property(get_fecha, set_fecha, None, None)
