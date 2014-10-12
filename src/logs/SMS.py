# -*- encoding: utf-8 -*-

import time
from suds.client import Client

class SMS(object):
    """
    La clase SMS disponibiliza las funciones para envío de notificaciones vía SMS
    """
    
    __urlSMS= None
    
    def __init__(self, hostSMS, puertoSMS):
        """Constructor de la clase SMS.
        @type urlSMS: String
        @param urlSMS: url para invocar el servicio web para envío de SMS"""
        self.__urlSMS= hostSMS+':'+puertoSMS+'/?wsdl'

    def enviarSMS(self, logEvento):
        """Método para enviar SMS a todos los destinatarios asociados al logEvento pasado como parámetro"""
        tipoLogEvento= logEvento.get_tipo_log()
        listaDestinatarios= tipoLogEvento.get_lista_destinatarios()
        dispositivo= logEvento.get_dispositivo()
        if dispositivo == 0:
            nombreDispositivo= "Placa controladora"
        else:
            nombreDispositivo= dispositivo.get_nombre()
        mensaje= logEvento.get_mensaje()
        tipoMensaje= mensaje.get_tipo()
        smsEnvio= tipoMensaje+ """
Dispositivo: """+ nombreDispositivo+ """
"""+mensaje.get_texto()+"""
Fecha: """+str(logEvento.get_fecha())[0:19]
        print(smsEnvio)
        try:
            client = Client(self.__urlSMS)
            for destinatario in listaDestinatarios:
                horaActual= int(time.strftime("%H"))
                if horaActual >= destinatario.get_hora_min() and horaActual < destinatario.get_hora_max():
                    celular= destinatario.get_celular()
                    client.service.sendSMS(celular, smsEnvio)
        except:
            return 'F'
