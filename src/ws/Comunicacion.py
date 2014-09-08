# -*- encoding: utf-8 -*-
#from src.placa.Main import encenderActuador
import soaplib.core
from soaplib.core.model.primitive import String, Integer
from soaplib.core.server import wsgi
from soaplib.core.model.clazz import Array
from soaplib.core.service import DefinitionBase
from soaplib.core.service import soap
from src.logs.Mensaje import Mensaje
from src.bdd.ManejadorBD import ManejadorBD
from src.recursos import Mensajes
from soaplib.core.model.primitive import String, Integer
from src.placa.Main import encenderActuador



class Comunicacion(DefinitionBase):
    """
    Clase que inicia el servidor de servicios web
    """
    """__placa= None

    def __init__(self, placa):
        self.__placa= placa"""

    @soap(Integer,_returns=String)
    def encenderGrupoActuadores(self, idGrupo):
        listaGrupoActuadores= self.__placa.get_lista_grupo_actuadores()
        mensaje= None
        grupo=None
        i=0
        while i < len(listaGrupoActuadores) and idGrupo <> listaGrupoActuadores[i].get_id_grupo_actuador():
            i= i+1
        if i < len(listaGrupoActuadores):
            grupo= listaGrupoActuadores[i]
            resultado=encenderActuador(grupo)
            mensaje= resultado.get_mensaje()
        else:
            print ('No existe grupo de actuadores')
            idMensaje= Mensajes.noExisteGrupoActuadores
            mbd= ManejadorBD()
            con= mbd.getConexion()
            mensaje=mbd.obtenerMensaje(con, idMensaje)
            con.close()
        return mensaje.get_texto()


        
        