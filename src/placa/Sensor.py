# -*- encoding: utf-8 -*-
from src.placa.Dispositivo import Dispositivo

class Sensor(Dispositivo):
    """
    La clase sensor se utiliza para representar un dispositivo de tipo sensor.
    Además de los atributos de un dispositivo tiene un atributo formulaConversion
    de tipo String, que se utiliza para obtener la formula de conversión entre su lectura bruta
    y el valor que esta representa en su respectiva unidad; y un atributo tipoPuerto que indica 
    si está conectado a un puerto analógico, digital de entrada ó digital de salida
    """

    __formulaConversion= None
    __tipoPuerto= None
    
    def __init__(self, idDispositivo, nombre, modelo, numeroPuerto, activoSistema, padre, formulaConversion, tipoPuerto):
        """
        Constructor de un sensor, recibe como parámetros:
            -idDispositivo : int (dispositivo)
            -nombre: String (dispositivo)
            -modelo: String (dispositivo)
            -numeroPuerto: int (dispositivo)
            -activoSistema: Boolean (dispositivo)
            -formulaConversion: String (sensor)
            -tipoPuerto: tipoPuerto (sensor)
        """
        Dispositivo.__init__(self, 
            idDispositivo, nombre, modelo, numeroPuerto, activoSistema, padre)
        self.__formulaConversion = formulaConversion
        self.__tipoPuerto = tipoPuerto

    def get_formula_conversion(self):
        """
        Devuelve la formula de conversión de un sensor como un String
        """
        return self.__formulaConversion
    
    def get_tipo_puerto(self):
        """
        Devuelve el tipo de puerto en el que está conectado un sensor como un tipoPuerto
        """
        return self.__tipoPuerto


    def set_formula_conversion(self, value):
        """
        Asigna un String a la formula de conversión de un sensor
        """
        self.__formulaConversion = value
        
    def set_tipo_puerto(self, value):
        """
        Asigna un tipoPuerto como el tipo de puerto al que está conectado un sensor
        """
        self.__tipoPuerto = value

    formulaConversion = property(get_formula_conversion, set_formula_conversion, None, None)
    tipoPuerto = property(get_tipo_puerto, set_tipo_puerto, None, None)




    
        