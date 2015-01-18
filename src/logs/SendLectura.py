# -*- encoding: utf-8 -*-

from suds.client import Client


class SendLectura(object):
    """
    La clase SMS disponibiliza las funciones para envío de notificaciones vía SMS
    """
    __urlAC= None
    
    def __init__(self, hostAC, puertoAC):
        """Constructor de la clase SMS.
        @type urlSMS: String
        @param urlSMS: url para invocar el servicio web para envío de SMS"""
        self.__urlAC= hostAC+':'+puertoAC+'/SGIA-web/sgia_AC_ws?wsdl'
   
    def enviarLecturas(self, nroSerie, listaLecturas):
        """Método utilizado para invocar al ws en la aplicacion centralizadora para enviar las lecturas obtenidas en la PC."""
        try:
            client = Client(self.__urlAC)
            listaWS= list()
            for lectura in listaLecturas:
                res1= {}
                res1['fecha']=lectura.get_fecha()
                res1['lectura']=lectura.get_lectura()
                res1['idDispositivo']= lectura.get_id_dispositivo()
                listaWS.append(res1)
            ok=False
            ok=client.service.inLecturas(nroSerie, listaWS)
        except:
            print('Error informando Lecturas')
            return False
        return ok
    
    def enviarLecturasFactor(self, nroSerie, listaLecturas):
        """Método utilizado para invocar al ws en la aplicacion centralizadora para enviar las lecturas de los factores obtenidas en la PC."""
        try:
            client = Client(self.__urlAC)
            listaWS= list()
            for lectura in listaLecturas:
                res1= {}
                res1['fecha']=lectura.get_fecha()
                res1['lectura']=lectura.get_lectura()
                res1['idDispositivo']= lectura.get_id_dispositivo()
                listaWS.append(res1)
            ok=False
            ok=client.service.inLecturasFactor(nroSerie, listaWS)
        except:
            print('Error informando Lecturas')
            return False
        return ok
    
    def enviarAcciones(self, nroSerie, listaAcciones):
        """Método utilizado para invocar al ws en la aplicacion centralizadora para enviar las acciones disparadas en la PC."""
        try:
            client = Client(self.__urlAC)
            listaWS= list()
            for accion in listaAcciones:
                res1= {}
                res1['fecha']=accion.get_fecha()
                res1['tipoAccion']=accion.get_tipo_accion()
                res1['idDispositivo']= accion.get_id_dispositivo()
                listaWS.append(res1)
            ok=False
            ok=client.service.inAcciones(nroSerie, listaWS)
        except:
            print('Error informando Acciones')
            return False
        return ok
    
    def enviarLogEvento(self, nroSerie, logEvento):
        """Método utilizado para invocar al ws en la aplicacion centralizadora para enviar un Log Evento."""
        try:
            client = Client(self.__urlAC)
            
            res1= {}
            res1['fecha']=logEvento.get_fecha()
            res1['tipoLog']=logEvento.get_tipo_log().get_id_tipo_log_evento()
            res1['idDispositivo']= logEvento.get_dispositivo().get_id_dispositivo()
            res1['idMensaje']= logEvento.get_mensaje().get_id_mensaje()
                
            ok=False
            ok=client.service.inLogEvento(nroSerie, res1)
        except:
            print('Error informando Acciones')
            return False
        return ok
    
    def enviarLogEventoPendientes(self, nroSerie, listaLogEvento):
        """Método utilizado para invocar al ws en la aplicacion centralizadora para enviar un Log Evento."""
        try:
            client = Client(self.__urlAC)
            
            listaWS= list()
            for logEvento in listaLogEvento:
                res1= {}
                res1['fecha']=logEvento.get_fecha()
                res1['tipoLog']=logEvento.get_tipo_log()
                res1['idDispositivo']= logEvento.get_id_dispositivo()
                res1['idMensaje']= logEvento.get_id_mensaje()
                listaWS.append(res1)
            ok=False
            ok=client.service.inLogEventosPendientes(nroSerie, listaWS)
        except:
            print('Error informando Acciones')
            return False
        return ok
    
