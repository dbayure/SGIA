# -*- encoding: utf-8 -*-
    

from gsmmodem.modem import GsmModem
import time
import logging
from suds.client import Client

urlSMS= 'http://192.168.0.101:7789/?wsdl'

class SMS(object):
    """
    La clase SMS disponibiliza las funciones para envío de notificaciones vía SMS
    """

    def enviarSMS(self, logEvento):
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
            #logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
            client = Client(urlSMS)
            
            
            for destinatario in listaDestinatarios:
                horaActual= int(time.strftime("%H"))
                if horaActual >= destinatario.get_hora_min() and horaActual < destinatario.get_hora_max():
                    celular= destinatario.get_celular()
                    resWS =  client.service.sendSMS(celular, smsEnvio)

        except:
            return 'F'
        
            
