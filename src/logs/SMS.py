# -*- encoding: utf-8 -*-
    
from __future__ import print_function
PORT = '/dev/ttyUSB0'
BAUDRATE = 115200
PIN = 8152 # SIM card PIN (if any)
from gsmmodem.modem import GsmModem
import time

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
            modem= GsmModem(PORT, BAUDRATE)
            intensidad= modem.signalStrength()
            if intensidad <= 0:
                return 'F'
            else:
                modem.smsTextMode = False
                modem.connect(PIN)
               
                for destinatario in listaDestinatarios:
                    horaActual= int(time.strftime("%H"))
                    if horaActual >= destinatario.get_hora_min() and horaActual < destinatario.get_hora_max():
                        celular= destinatario.get_celular()
                        modem.sendSms(celular, smsEnvio)
                modem.close()
        except:
            return 'F'
        
            
