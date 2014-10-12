# -*- encoding: utf-8 -*-
from src.placa.Dispositivo import Dispositivo

class Sensor(Dispositivo):
    """
    La clase sensor se utiliza para representar un dispositivo de tipo sensor.
    Además de los atributos de un dispositivo tiene un atributo formulaConversion de tipo String, que se utiliza para obtener la formula de conversión entre su lectura bruta
    y el valor que esta representa en su respectiva unidad; y un atributo tipoPuerto que indica si está conectado a un puerto analógico, digital de entrada ó digital de salida.
    """

    __formulaConversion= None
    __tipoPuerto= None
    
    def __init__(self, idDispositivo, nombre, modelo, numeroPuerto, activoSistema, padre, estadoAlerta, formulaConversion, tipoPuerto):
        """
        Constructor de un sensor.
        @type idDispositivo: int
        @param idDispositivo: Identificador del actuador
        @type nombre: String
        @param nombre: Nombre del dispositivo
        @type modelo: String
        @param modelo: Modelo del dispositivo
        @type numeroPuerto: int
        @param numeroPuerto: Número de puerto al que está conectado el dispositivo
        @type activoSistema: Char(1)
        @param activoSistema: Indicador del estado del dispositivo en el sistema. (S/N)
        @type padre: int
        @param padre: Identificador del dispositivo padre
        @type estadoAlerta: Char(1)
        @param estadoAlerta: Indicador si el dispositivo está en estado de alerta. (S/N)
        @type formulaConversion: String
        @param formulaConversion: Formula matemática para conversión desde una lectura bruta al valor según la unidad del factor al que pertenece el sensor. Debe cumplir el formato matemático de Python.
        @type tipoPuerto: TipoPuerto
        @param tipoPuerto: Tipo de puerto al que está conectado el sensor."""
        Dispositivo.__init__(self, idDispositivo, nombre, modelo, numeroPuerto, activoSistema, padre, estadoAlerta)
        self.__formulaConversion = formulaConversion
        self.__tipoPuerto = tipoPuerto

    def get_formula_conversion(self):
        """
        @rtype: String
        @return: Devuelve la formula de conversión de un sensor.
        """
        return self.__formulaConversion
    
    def get_tipo_puerto(self):
        """
        @rtype: TipoPuerto
        @return: Devuelve el tipo de puerto al que está conectado el sensor."""
        return self.__tipoPuerto

    def set_formula_conversion(self, value):
        """Asigna un String como la formula de conversión de el sensor."""
        self.__formulaConversion = value
        
    def set_tipo_puerto(self, value):
        """Asigna un TipoPuerto como el tipo de puerto al que está conectado el sensor."""
        self.__tipoPuerto = value

    formulaConversion = property(get_formula_conversion, set_formula_conversion, None, None)
    tipoPuerto = property(get_tipo_puerto, set_tipo_puerto, None, None)
