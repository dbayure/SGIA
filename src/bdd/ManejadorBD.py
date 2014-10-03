# -*- encoding: utf-8 -*-
from src.recursos import Propiedades
import sqlite3
from src.bdd.Consultas import Consultas
from _sqlite3 import Connection
from src.placa.TipoPuerto import TipoPuerto
from src.placa.Sensor import Sensor
from src.placa.TipoActuador import TipoActuador
from src.placa.Actuador import Actuador
from src.placa.TipoPlaca import TipoPlaca
from src.placa.PlacaAuxiliar import PlacaAuxiliar
from src.nivelesPerfiles.Factor import Factor
from src.nivelesPerfiles.GrupoActuadores import GrupoActuadores
from src.recursos.Herramientas import Herramientas
from src.logs.Mensaje import Mensaje
from Phidgets.PhidgetException import PhidgetException
from src.nivelesPerfiles.PerfilActivacion import PerfilActivacion
from src.nivelesPerfiles.NivelSeveridad import NivelSeveridad
from src.placa.ActuadorAvance import ActuadorAvance
from src.placa.Posicion import Posicion
from src.logs.Destinatario import Destinatario
from src.logs.TipoLogEventos import TipoLogEventos


class ManejadorBD(object):
    """
    Clase utilizada para acceder a la base de datos sqlite, y disponibilizar las estructuras de esta para la
    capa lógica de la aplicación.
    """
    
    __path= None
    __conexion= None


    def __init__(self):
        """
        Constructor de la clase ManejadorBD. No recibe parámetros, pero genera una nueva instancia de conexion,
        y lee desde el archivo de propiedades el path de la base de datos.
        """
        self.__path= Propiedades.pathBD
        
    def getConexion(self):
        """
        Devuelve la conexion como un objeto Connection
        """
        self.__conexion= sqlite3.connect(self.__path)
        return self.__conexion
    
    def cerrarConexion(self):
        """
        Cierra la conexión a la base de datos
        """
        self.__conexion.close()
        return None
        
    def obtenerEstadoPlaca(self, conexion):
        """
        Devuelve es estado de la placa, como un char(1), este puede ser: 
        I=Inactivo, C=Configuración, M=Manual o A=Automático
        """
        c= Consultas()
        cursor= conexion.cursor()
        cursor.execute(c.selectEstadoPlaca())
        resultado= cursor.fetchone()
        cursor.close()
        return resultado[0]
    
    def obtenerNroSeriePlaca(self, conexion):
        """
        Devuelve el número de serie de la placa, como un String
        """
        c= Consultas()
        cursor= conexion.cursor()
        cursor.execute(c.selectNroSeriePlaca())
        resultado= cursor.fetchone()
        cursor.close()
        return resultado[0]
    
    def obtenerPeriodicidadLecturasPlaca(self, conexion):
        """
        Devuelve el número de serie de la placa, como un String
        """
        c= Consultas()
        cursor= conexion.cursor()
        cursor.execute(c.selectPeriodicidadLecturaPlaca())
        resultado= cursor.fetchone()
        cursor.close()
        return resultado[0]
    
    def obtenerPeriodicidadNivelesPlaca(self, conexion):
        """
        Devuelve el número de serie de la placa, como un String
        """
        c= Consultas()
        cursor= conexion.cursor()
        cursor.execute(c.selectPeriodicidadNivelesPlaca())
        resultado= cursor.fetchone()
        cursor.close()
        return resultado[0]
    
   
    def __obtenerListaPosicionesActuadorAvance(self, conexion, idActuadorAvance):
        c= Consultas()
        cursor= conexion.cursor()
        cursor.execute(c.selectPosicionesActuadorAvance(), (idActuadorAvance,))
        listaPosiciones= list()
        for fila in cursor:
            posicion= fila[0]
            descripcion= fila[1]
            valor= fila[2]
            pos= Posicion(posicion, descripcion, valor, None)
            listaPosiciones.append(pos)
        cursor.close()
        return listaPosiciones
       
    def __cargarSensores(self, lista, conexion, idPadre=-1):
        c= Consultas()
        cursor= conexion.cursor()
        if idPadre < 0:
            cursor.execute(c.selectSensoresActivosPlacaPadre())
        else:
            cursor.execute(c.selectSensoresActivosPlacaAux(), (idPadre,))
        for fila in cursor:
            idDispositivo= fila[0]
            nombre= fila[1]
            modelo= fila[2]
            nroPuerto= fila[3]
            activoSistema= fila[4]
            formulaConversion= fila[5]
            idTipoPuerto=fila[6]
            cursorAux= conexion.cursor()
            cursorAux.execute(c.selectTipoPuerto(), (idTipoPuerto,))
            resAux= cursorAux.fetchone()
            nombreTipoPuerto= resAux[0]
            cursorAux.close()
            tipoPuerto= TipoPuerto(idTipoPuerto, nombreTipoPuerto)
            sensor= Sensor(idDispositivo, nombre, modelo, nroPuerto, activoSistema, None, formulaConversion, tipoPuerto)
            lista.append(sensor)
        return None
    
    def __cargarActuadores(self, lista, conexion, idPadre=-1):
        c= Consultas()
        cursor= conexion.cursor()
        if idPadre < 0:
            cursor.execute(c.selectActuadoresActivosPlacaPadre())
        else:
            cursor.execute(c.selectActuadoresActivosPlacaAux(), (idPadre,))
        for fila in cursor:
            idDispositivo= fila[0]
            nombre= fila[1]
            modelo= fila[2]
            nroPuerto= fila[3]
            activoSistema= fila[4]
            estado= fila[5]
            idTipoPuerto=fila[6]
            idTipoActuador=fila[7]
            cursorAux= conexion.cursor()
            cursorAux.execute(c.selectTipoPuerto(), (idTipoPuerto,))
            resAux= cursorAux.fetchone()
            nombreTipoPuerto= resAux[0]
            cursorAux.execute(c.selectTipoActuador(), (idTipoActuador,))
            resAux= cursorAux.fetchone()
            nombreTipoActuador= resAux[0]
            cursorAux.close()
            tipoPuerto= TipoPuerto(idTipoPuerto, nombreTipoPuerto)
            tipoActuador= TipoActuador(idTipoActuador, nombreTipoActuador)
            actuador= Actuador(idDispositivo, nombre, modelo, nroPuerto, activoSistema, None, estado, tipoActuador, tipoPuerto)
            lista.append(actuador)
        return None
    
    def __cargarActuadoresAvance(self, lista, conexion, idPadre=-1):
        c= Consultas()
        cursor= conexion.cursor()
        if idPadre < 0:
            cursor.execute(c.selectActuadoresAvanceActivosPlacaPadre())
            
        else:
            cursor.execute(c.selectActuadoresAvanceActivosPlacaAux(), (idPadre,))
        for fila in cursor:
            idDispositivo= fila[0]
            nombre= fila[1]
            modelo= fila[2]
            nroPuerto= fila[3]
            activoSistema= fila[4]
            posicion= fila[5]
            idTipoPuerto=fila[6]
            idTipoActuador=fila[7]
            nroPuertoRetroceso=fila[8]
            idTipoPuertoRetroceso=fila[9]
            tiempoEntrePosiciones=fila[10]
            cursorAux= conexion.cursor()
            cursorAux.execute(c.selectTipoPuerto(), (idTipoPuerto,))
            resAux= cursorAux.fetchone()
            nombreTipoPuerto= resAux[0]
            cursorAux.execute(c.selectTipoPuerto(), (idTipoPuertoRetroceso,))
            resAux= cursorAux.fetchone()
            nombreTipoPuertoRetroceso= resAux[0]
            cursorAux.execute(c.selectTipoActuador(), (idTipoActuador,))
            resAux= cursorAux.fetchone()
            nombreTipoActuador= resAux[0]
            
            tipoPuerto= TipoPuerto(idTipoPuerto, nombreTipoPuerto)
            tipoPuertoRetroceso= TipoPuerto(idTipoPuertoRetroceso, nombreTipoPuertoRetroceso)
            tipoActuador= TipoActuador(idTipoActuador, nombreTipoActuador)
            listaPosiciones= self.__obtenerListaPosicionesActuadorAvance(conexion, idDispositivo)
            
            actuadorAvance= ActuadorAvance(idDispositivo, nombre, modelo, nroPuerto, activoSistema, None, posicion, tipoActuador, tipoPuerto, nroPuertoRetroceso, tipoPuertoRetroceso, tiempoEntrePosiciones, listaPosiciones)
            lista.append(actuadorAvance)
            cursorAux.close()
        return None
    
    def obtenerListaIdSensoresPosicion(self, conexion, idDispositivo, idPosicion):
        c= Consultas()
        cursor= conexion.cursor()
        cursor.execute(c.selectSensoresPosicion(), (idDispositivo, idPosicion))
        listaIds=list()
        for fila in cursor:
            listaIds.append(fila[0])
        cursor.close()
        return listaIds
    
    def __cargarPlacasAuxiliares(self, lista, conexion, idPadre=-1):
        c= Consultas()
        cursor= conexion.cursor()
        if idPadre < 0:
            cursor.execute(c.selectPlacasAuxiliaresActivasPlacaPadre())
        else:
            cursor.execute(c.selectPlacasAuxiliaresActivasPlacaAux(), (idPadre,))
        for fila in cursor:
            idDispositivo= fila[0]
            nombre= fila[1]
            modelo= fila[2]
            nroPuerto= fila[3]
            activoSistema= fila[4]
            nroSerie= fila[5]
            idTipoPlaca=fila[6]
            cursorAux= conexion.cursor()
            cursorAux.execute(c.selectTipoPlaca(), (idTipoPlaca,))
            resAux= cursorAux.fetchone()
            nombreTipoPlaca= resAux[0]
            cursorAux.close()
            tipoPlaca= TipoPlaca(idTipoPlaca, nombreTipoPlaca)
            #creo mi lista de dispositivos
            l= list()
            self.__cargarSensores(l, conexion, idDispositivo)
            self.__cargarActuadores(l, conexion, idDispositivo)
            self.__cargarActuadoresAvance(l, conexion, idDispositivo)
            self.__cargarPlacasAuxiliares(l, conexion, idDispositivo)
            placaAuxiliar= PlacaAuxiliar(idDispositivo, nombre, modelo, nroPuerto, activoSistema, None, nroSerie, tipoPlaca, l)
            h= Herramientas()
            ik= h.instanciarIK(int(nroSerie))
            placaAuxiliar.set_ik(ik)
            if ik == None:
                print('No se pudo instanciar el ik de la placa auxiliar')
            for dispositivo in l:
                dispositivo.set_padre(placaAuxiliar)
            lista.append(placaAuxiliar)
        return None
       
    def obtenerListaDispositivos(self, conexion):
        """
        Devuelve la lista de todos los dispositivos activos del sistema
        """
        l= list()
        #1. Obtener lista sensores conectados directamente a la placa padre
        self.__cargarSensores(l, conexion)
        #2. obtener lista actuadores conectados directamente a la placa controladora
        self.__cargarActuadores(l, conexion)
        #3. obtener lista de actuadores de avance
        self.__cargarActuadoresAvance(l, conexion)
        #4. obtener lista placas auxiliares
        self.__cargarPlacasAuxiliares(l, conexion)
        return l
    
    def obtenerListaFactores(self, conexion):
        """
        Devuelve una lista con todos los factores activos en el sistema
        """
        lista= list()
        c= Consultas()
        cursor= conexion.cursor()
        cursor.execute(c.selectFactores())
        for fila in cursor:
            idFactor= fila[0]
            nombre= fila[1]
            unidad= fila[2]
            valorMin= fila[3]
            valorMax= fila[4]
            umbral= fila[5]
            activoSistema= fila[6]
            factor= Factor(idFactor, nombre, unidad, valorMin, valorMax, umbral, None, activoSistema)
            lista.append(factor)
        cursor.close()
        return lista
        
    def obtenerListaIdSensoresFactor(self, conexion, idFactor):
        """
        Devuelve la lista de id de dispositivos sensores pertenecientes al factor pasado
        como parámetro
        """
        lista= list()
        c= Consultas()
        cursor= conexion.cursor()
        cursor.execute(c.selectIdSensoresFactor(), (idFactor,))
        for fila in cursor:
            idSensor= fila[0]
            lista.append(idSensor)
        cursor.close()
        return lista
    
    def obtenerListaGrupoActuadores(self, conexion):
        """
        Devuelve una lista con todos los grupos de actuadores activos en el sistema
        """
        lista= list()
        c= Consultas()
        cursor= conexion.cursor()
        cursor.execute(c.selectGruposActuadoresActivos())
        for fila in cursor:
            idGrupoActuador= fila[0]
            estado= fila[1]
            nombre= fila[2]
            deAvance= fila[3]
            activoSistema= fila[4]
            grupo= GrupoActuadores(idGrupoActuador, estado, nombre, None, deAvance, activoSistema)
            lista.append(grupo)
        cursor.close()
        return lista
        
    def obtenerListaIdActuadoresGrupo(self, conexion, idGrupo, deAvance):
        """
        Devuelve la lista de id de dispositivos sensores pertenecientes al factor pasado
        como parámetro
        """
        lista= list()
        c= Consultas()
        cursor= conexion.cursor()
        if deAvance == 'N':
            cursor.execute(c.selectIdActuadoresGrupo(), (idGrupo,))
            for fila in cursor:
                idActuador= fila[0]
                lista.append(idActuador)
        else:
            cursor.execute(c.selectIdActuadoresAvanceGrupo(), (idGrupo,))
            for fila in cursor:
                idActuadorAvance= fila[0]
                lista.append(idActuadorAvance)
        cursor.close()
        return lista
    
    def obtenerListaNivelesSeveridad(self, conexion):
        """
        Devuelve una lista con todos los niveles de severidad activos en el sistema
        """
        lista= list()
        c= Consultas()
        cursor= conexion.cursor()
        cursor.execute(c.selectObtenerNivelesSeveridad())
        for fila in cursor:
            idNivel= fila[0]
            nombre= fila[1]
            idFactor= fila[2]
            prioridad= fila[3]
            rangoMinimo= fila[4]
            rangoMaximo= fila[5]
            idPerfilActivacion= fila[6]
            perfilActivacion= PerfilActivacion(idPerfilActivacion, None)
            activoSistema= fila[7]
            nivel= NivelSeveridad(idNivel, nombre, idFactor, prioridad, rangoMinimo, rangoMaximo, perfilActivacion, activoSistema)
            lista.append(nivel)
        cursor.close()
        return lista
    
    def obtenerListaIdGruposActuadoresEstadosPerfil(self, conexion, idPerfil):
        """
        Obtiene una lista de tuplas compuestas por el id del grupo de actuadores y el estado que se pretende del mismo
        dentro del perfil de activación
        """
        lista= list()
        c= Consultas()
        cursor= conexion.cursor()
        cursor.execute(c.selectIdGruposActuadoresEstadosActivosPerfil(), (idPerfil,))
        for fila in cursor:
            idGrupoActuadores= fila[0]
            estado= fila[1]
            tupla= (idGrupoActuadores, estado)
            lista.append(tupla)
        cursor.close()
        return lista
    
    
    
    def cambiarEstadoActuador(self, conexion, actuador):
        c= Consultas()
        cursor= conexion.cursor()
        cursor.execute(c.updateEstadoActuador(), (actuador.get_estado_actuador(), actuador.get_id_dispositivo()))
        cursor.close()    
        return None
    
    def cambiarPosicionActuadorAvance(self, conexion, actuadorAvance):
        c= Consultas()
        cursor= conexion.cursor()
        cursor.execute(c.updatePosicionActuadorAvance(), (actuadorAvance.get_posicion(), actuadorAvance.get_id_dispositivo()))
        cursor.close()    
        return None
    
    def cambiarEstadoGrupoActuadores(self, conexion, grupoActuadores):
        c= Consultas()
        cursor= conexion.cursor()
        cursor.execute(c.updateEstadoGrupoActuadores(), (grupoActuadores.get_estado(), grupoActuadores.get_id_grupo_actuador()))
        cursor.close()    
        return None
        
    
    def obtenerHostWS(self, conexion):
        """
        Devuelve el Host en el que está publicado el servidor de servicios web de la placa controladora,
        como un String
        """
        return None
    
    def obtenerPuertoWS(self, conexion):
        """
        Devuelve el puerto en el que está publicado el servidor de servicios web de la placa controladora,
        como un int
        """
        return None
    
    def insertarSensor(self, conexion, idDispositivo, formulaConversion, idTipoPuerto, idPlacaPadre, idFactor):
        """
        Inserta un sensor en la base de datos, recibe como parámetros la conexión a la base y el sensor a insertar.
        """
        c= Consultas()
        cursor= conexion.cursor()
        cursor.execute(c.insertSensor(), (idDispositivo, formulaConversion, idTipoPuerto, idPlacaPadre, idFactor))
        cursor.close()  
        return None
    
    def insertarTipoPlaca(self, conexion, nombre):
        """
        Inserta un tipo de placa en la base de datos y devuelve su id.
        """
        c= Consultas()
        cursor= conexion.cursor()
        cursor.execute(c.insertTipoPlaca(), (nombre,))
        cursor.close()  
        conexion.commit()
        cursor= conexion.cursor()
        cursor.execute(c.selectUltimoTipoPlaca())
        resultado= cursor.fetchone()
        cursor.close()        
        return resultado[0]
        return None
    
    def insertarTipoActuador(self, conexion, nombre):
        """
        Inserta un tipo de actuador en la base de datos y devuelve su id.
        """
        c= Consultas()
        cursor= conexion.cursor()
        cursor.execute(c.insertTipoActuador(), (nombre,))
        cursor.close()  
        conexion.commit()
        cursor= conexion.cursor()
        cursor.execute(c.selectUltimoTipoActuador())
        resultado= cursor.fetchone()
        cursor.close()        
        return resultado[0]
        return None
    
    def insertarActuador(self, conexion, idDispositivo, idTipoPuerto, idTipoActuador, idPlacaPadre, idGrupoActuadores):
        """
        Inserta un actuador en la base de datos, recibe como parámetros la conexión a la base y el actuador a insertar.
        """
        c= Consultas()
        cursor= conexion.cursor()
        cursor.execute(c.insertActuador(), (idDispositivo, idTipoPuerto, idTipoActuador, idPlacaPadre, idGrupoActuadores))
        cursor.close()  
        return None
    
    def insertarActuadorAvance(self, conexion, idDispositivo, posicion, idTipoPuerto, idTipoActuador, idPlacaPadre, nroPuertoRetroceso, tipoPuertoRetroceso, tiempoEntrePosiciones, idGrupoActuadores):
        """
        Inserta un actuador en la base de datos, recibe como parámetros la conexión a la base y el actuador a insertar.
        """
        c= Consultas()
        cursor= conexion.cursor()
        cursor.execute(c.insertActuadorAvance(), (idDispositivo, posicion, idTipoPuerto, idTipoActuador, idPlacaPadre, nroPuertoRetroceso, tipoPuertoRetroceso, tiempoEntrePosiciones, idGrupoActuadores))
        cursor.close()  
        return None
    
    def insertarPosicionActuadorAvance(self, conexion, idActuadorAvance, numeroPosicion, descripcion, valor):
        """
        Inserta una posicion a un actuador de avance en la base de datos.
        """
        c= Consultas()
        cursor= conexion.cursor()
        cursor.execute(c.insertPosicion(), (idActuadorAvance, numeroPosicion, descripcion, valor))
        cursor.close()  
        return None
    
    def insertarSensorPosicionActuadorAvance(self, conexion, idSensor, idActuadorAvance, numeroPosicion):
        """
        Inserta una posicion a un actuador de avance en la base de datos.
        """
        c= Consultas()
        cursor= conexion.cursor()
        cursor.execute(c.insertSensorPosicion(), (idSensor, idActuadorAvance, numeroPosicion))
        cursor.close()  
        return None
    
    def cambiarEstadoPlaca(self, conexion, estado):
        """
        Actualiza el estado del sistema.
        Estos puede ser: I=Inactivo, C=Configuración, M=Manual o A=Automático
        """
        c= Consultas()
        cursor= conexion.cursor()
        cursor.execute(c.updateEstadoPlaca(), (estado,))
        return None

    
    def existeSensor(self, conexion, idSensor):
        """
        Consulta si existe sensor en la base de datos con el identificador de dispositivo pasado como parámetro.
        Recibe la conexión a la base de datos y el identificador de dispositivo correspondiente al sensor.
        Devuelve un boolean.
        """
        return None
    
    def existeActuador(self, conexion, idActuador):
        """
        Consulta si existe actuador en la base de datos con el identificador de dispositivo pasado como parámetro.
        Recibe la conexión a la base de datos y el identificador de dispositivo correspondiente al actuador
        Devuelve un boolean.
        """
        return None
    
    def insertarPlacaAuxiliar(self, conexion, idDispositivo, nroSerie, idTipoPlaca, idPlacaPadre):
        """
        Inserta una placa auxiliar en la base de datos.
        Recibe como parámetros la conexión a la base y la placa auxiliar a insertar.
        """
        c= Consultas()
        cursor= conexion.cursor()
        cursor.execute(c.insertPlacaAuxiliar(), (idDispositivo, nroSerie, idTipoPlaca, idPlacaPadre))
        cursor.close()  
        return None
    
    def existePlacaAuxiliar(self, conexion, idActuador):
        """
        Consulta si existe actuador en la base de datos con el identificador de dispositivo pasado como parámetro.
        Recibe la conexión a la base de datos y el identificador de dispositivo correspondiente al actuador
        Devuelve un boolean.
        """
        return None
    
    def eliminadoLogicoPlacaAuxiliar(self, conexion, idPlacaAuxiliar):
        """
        Elimina lógicamente una placa auxiliar del sistema, esta operación consiste en cambiar su atributo activoSistema.
        Recibe como parámetros la conexión a la base de datos y el id del dispositivo placa auxiliar a eliminar.
        """
        return None
    
    def insertarLecturaSensor(self, conexion, idSensor, lectura):
        """
        Inserta en base de datos una lectura de un sensor.
        Recibe como parámetros la conexión a la base el id de dispositivo del sensor y la lectura obtenida
        """
        c= Consultas()
        cursor= conexion.cursor()
        cursor.execute(c.insertLecturaSensor(), (idSensor, lectura))
        cursor.close()        
        return None
    
    def insertarLecturaFactor(self, conexion, idFactor, fecha, lectura):
        """
        Inserta en base de datos una lectura de un factor.
        Recibe como parámetros la conexión a la base el id de dispositivo del sensor y la lectura obtenida
        """
        c= Consultas()
        cursor= conexion.cursor()
        cursor.execute(c.insertLecturaFactor(), (idFactor, fecha, lectura))
        cursor.close()        
        return None
    
    def obtenerLecturasFactorFecha(self, conexion, idFactor, fechaMin, fechaMax):
        """
        Obtiene todas las lecturas pertenecientes al factor pasado como parámetro entre las fechas
        pasadas como parámetros. Recibe como parámetros la conexión a la base, el id del factor, la fecha minima
        y la fecha máxima a considerar.
        Devuelve una lista de resultado de lecturas
        """
        return None
    
    def obtenerLecturasFactorCantidad(self, conexion, idFactor, numeroLecturas):
        """
        Obtiene las últimas n lecturas indicadas en el parámetro numeroLecturas para el factor pasado como parámetro
        Recibe como parámetros la conexión a la base, el id del factor y el número de lecturas a obtener
        Devuelve una lista de resultado de lecturas
        """
        c= Consultas()
        cursor= conexion.cursor()
        cursor.execute(c.selectLecturasPorCantidad(), (idFactor, numeroLecturas))
        listaValoresLecturas= list()
        for lectura in cursor:
            listaValoresLecturas.append(lectura[0])
        cursor.close()   
        return listaValoresLecturas
    
    def insertarAccionActuador(self, conexion, idActuador, accion):
        """
        Inserta en la base de datos una acción disparada sobre un actuador.
        Recibe como parámetros la conexión a la base, el actuador
        """
        c= Consultas()
        cursor= conexion.cursor()
        cursor.execute(c.insertAccionActuador(), (idActuador, accion))
        cursor.close()        
        return None

    
    def insertarFactor(self, conexion, nombre, unidad, valorMin, valorMax, umbral):
        """
        Inserta en la base de datos un factor pasado como parámetro.
        Recibe como parámetros la conexión a la base y el factor a insertar
        """
        c= Consultas()
        cursor= conexion.cursor()
        cursor.execute(c.insertFactor(), (nombre, unidad, valorMin, valorMax, umbral, 'S'))
        cursor.close()
        conexion.commit()
        cursor= conexion.cursor()
        cursor.execute(c.selectUltimoFactor())
        resultado= cursor.fetchone()
        cursor.close()        
        return resultado[0]
    
    def insertarDispositivo(self, conexion, nombre, modelo, nroPuerto):
        """
        Inserta en la base de datos un dispositivo, creado con los atributos pasados como parámetros.
        """
        c= Consultas()
        cursor= conexion.cursor()
        cursor.execute(c.insertDispositivo(), (nombre, modelo, nroPuerto, 'S'))
        cursor.close()
        conexion.commit()
        cursor= conexion.cursor()
        cursor.execute(c.selectUltimoDispositivo())
        resultado= cursor.fetchone()
        cursor.close()        
        return resultado[0]
    
    def eliminadoLogicoFactor(self, conexion, idFactor):
        """
        Elimina lógicamente un factor del sistema, esta operación consiste en cambiar su atributo activoSistema.
        Recibe como parámetros la conexión a la base de datos y el id del factor a eliminar.
        """
        c= Consultas()
        cursor= conexion.cursor()
        cursor.execute(c.updateActivoSistemaFactor(),(idFactor,))
        cursor.close()  
        return None
    
    def obtenerFactorId(self, conexion, idFactor):
        """
        Obtiene desde la base de datos el factor determinado por el identificador pasado como parámetro.
        Recibe como parámetros la conexión a la base y el id de factor a recuperar
        """
        return None
    
    def existeFactorNombre(self, conexion, nombreFactor):
        """
        Obtiene el id del factor con el nombre pasado como parámetro, si existe, sino un número negativo.
        Recibe como parámetros la conexión a la base y el nombre del factor a buscar.
        Devuelve el id de factor encontrado o un numero negativo.
        """
        return None
    
    def insertarGrupoActuadores(self, conexion, nombre, deAvance):
        """
        Inserta en la base de datos un grupo de actuadores pasado como parámetro.
        Recibe como parámetros la conexión a la base y el grupo de actuadores a insertar.
        """
        c= Consultas()
        cursor= conexion.cursor()
        if deAvance == 'N':
            cursor.execute(c.insertGrupoActuadores(), (nombre,))
        else:
            cursor.execute(c.insertGrupoActuadoresAvance(), (nombre,))
        cursor.close()
        conexion.commit()
        cursor= conexion.cursor()
        cursor.execute(c.selectUltimoGrupoActuadores())
        resultado= cursor.fetchone()
        cursor.close()        
        return resultado[0]

    
    def eliminadoLogicoGrupoActuadores(self, conexion, idGrupoActuadores):
        """
        Elimina lógicamente un grupo de actuadores del sistema, esta operación consiste en cambiar su atributo activoSistema.
        Recibe como parámetros la conexión a la base de datos y el id del grupo de actuadores a eliminar.
        """
        c= Consultas()
        cursor= conexion.cursor()
        cursor.execute(c.updateActivoSistemaGrupoActuadores(),(idGrupoActuadores,))
        cursor.close()  
        return None
    
    def eliminadoLogicoDispositivo(self, conexion, idDispositivo):
        """
        Elimina lógicamente un grupo de actuadores del sistema, esta operación consiste en cambiar su atributo activoSistema.
        Recibe como parámetros la conexión a la base de datos y el id del grupo de actuadores a eliminar.
        """
        c= Consultas()
        cursor= conexion.cursor()
        cursor.execute(c.updateActivoSistemaDispositivo(),(idDispositivo,))
        cursor.close()  
        return None
    
    def eliminadoLogicoNivelSeveridad(self, conexion, idNivelSeveridad):
        """
        Elimina lógicamente un nivel de severidad del sistema, esta operación consiste en cambiar su atributo activoSistema.
        Recibe como parámetros la conexión a la base de datos y el id del nivel de severidad a eliminar.
        """
        c= Consultas()
        cursor= conexion.cursor()
        cursor.execute(c.updateActivoSistemaNivelSeveridad(),(idNivelSeveridad,))
        cursor.close()  
        return None
    
    def eliminadoLogicoFilaPerfilActivacion(self, conexion, idPerfil, idGrupoActuadores):
        """
        Elimina lógicamente un nivel de severidad del sistema, esta operación consiste en cambiar su atributo activoSistema.
        Recibe como parámetros la conexión a la base de datos y el id del nivel de severidad a eliminar.
        """
        c= Consultas()
        cursor= conexion.cursor()
        cursor.execute(c.updateActivoSistemaPerfilActivacion(),(idPerfil, idGrupoActuadores))
        cursor.close()  
        return None
    
    def obtenerGrupoActuadores(self, conexion, idGrupoActuadores):
        """
        Obtiene desde la base de datos el grupo de actuadores determinado por el identificador pasado como parámetro.
        Recibe como parámetros la conexión a la base y el id del grupo de actuadores a recuperar
        """
        return None
    
    def existeGrupoActuadores(self, conexion, nombreGrupo):
        """
        Obtiene el id del grupo de actuadores con el nombre pasado como parámetro, si existe, sino un número negativo.
        Recibe como parámetros la conexión a la base y el nombre del grupo de actuadores a buscar.
        Devuelve el id del grupo de actuadores encontrado o un número negativo.
        """
        return None
    
    def insertarNivelSeveridad(self, conexion, nombre, idFactor, prioridad, rangoMinimo, rangoMaximo):
        """
        Inserta en la base de datos el nivel de severidad pasado como parámetro.
        Recibe como parámetros la conexión a la base y el nivel de severidad a insertar.
        """
        c= Consultas()
        cursor= conexion.cursor()
        cursor.execute(c.insertNivelSeveridad(), (nombre, idFactor, prioridad, rangoMinimo, rangoMaximo))
        cursor.close()  
        conexion.commit()
        cursor= conexion.cursor()
        cursor.execute(c.selectUltimoNivelSeveridad())
        resultado= cursor.fetchone()
        idNivel= resultado[0]
        cursor.execute(c.updateIdPerfilActivacion(), (idNivel, idNivel))
        cursor.close()  
        conexion.commit
        return idNivel
    
    def insertarFilaPerfilActivacion(self, conexion, idPerfilActivacion, idGrupoActuadores, estado):
        """
        Inserta en la base de datos una fila perteneciente a un perfil de activación.
        """
        c= Consultas()
        cursor= conexion.cursor()
        cursor.execute(c.insertPerfilActivacion(), (idPerfilActivacion, idGrupoActuadores, estado))
        cursor.close()  
        conexion.commit()
        cursor.close()  
        return None
    
    def eliminadoLogicoNivelPerfil(self, conexion, idNivelSeveridad):
        """
        Elimina lógicamente un nivel de severidad y su perfil de activación asociado del sistema, esta operación consiste en cambiar su atributo activoSistema.
        Recibe como parámetros la conexión a la base de datos y el id del nivel de severidad a eliminar.
        """
        return None
    
    def existeNivelSeveridad(self, conexion, idNivelSeveridad):
        """
        Verifica si existe un nivel de severidad definido en el sistema con el identificador pasado como parámetro.
        Recibe como parámetros la conexión a la base y el identificador del nivel de severidad a buscar.
        Devuelve un boolean.
        """
        return None
    
    def obtenerNivelesSeveridad(self, conexion):
        """
        Obtiene desde la base de datos todos los niveles de severidad activos en el sistema.
        Recibe como parámetro la conexión a la base.
        Devuelve una lista de niveles de severidad
        """
        return None
    
    def obtenerPerfilActivacion(self, conexion, idPerfilActivacion):
        """
        Obtiene desde la base de datos el perfil de activacion correspondiente al identificador pasado como parámetro.
        Recibe como parámetros la conexión a la base y el identificador del perfil de activación que se pretende obtener.
        Devuelve el perfil de activación solicitado.
        """
        return None
    
    def obtenerMensaje(self, conexion, idMensaje):
        """
        Obtiene desde la base de datos el mensaje correspondiente al identificador pasado como parámetro.
        Recibe como parámetros la conexión a la base y el identificador del mensaje que se pretende obtener.
        Devuelve el mensaje solicitado.
        """
        c= Consultas()
        cursor= conexion.cursor()
        cursor.execute(c.selectMensaje(), (idMensaje,))
        resultado= cursor.fetchone()
        cursor.close()
        idMensaje= resultado[0]
        tipo= resultado[1]
        texto= resultado[2]
        mensaje= Mensaje(idMensaje, tipo, texto)
        return mensaje
    
    def obtenerTipoLogEvento(self, conexion, idTipoLog):
        """
        Obtiene desde la base de datos el tipo de log de eventos que corresponde al id pasado como parámetro.
        """
        c= Consultas()
        cursor= conexion.cursor()
        cursor.execute(c.selectTipoLogEventos(), (idTipoLog,))
        resultado= cursor.fetchone()
        
        idTipoLogEvento= resultado[0]
        nombre= resultado[1]
        enviarSMS= resultado[2]
        enviarMAIL= resultado[3]
        listaDestinatarios= list()
        cursor.execute(c.selectListaDestinatarios(), (idTipoLogEvento,))
        for fila in cursor:
            idDestinatario= fila[0]
            nombreDestinatario= fila[1]
            celular= fila[2]
            mail= fila[3]
            horaMin= fila[4]
            horaMax= fila[5]
            destinatario= Destinatario(idDestinatario, nombreDestinatario, celular, mail, horaMin, horaMax)
            listaDestinatarios.append(destinatario)
        cursor.close()
        tipoLogEvento= TipoLogEventos(idTipoLogEvento, nombre, enviarSMS, enviarMAIL, listaDestinatarios)
        return tipoLogEvento
    
    def insertarLogEvento (self, conexion, idTipoLog, idDispositivo, idMensaje, fecha):
        """
        Inserta en la base de datos el log de evento pasado como parámetro.
        Recibe como parámetros la conexión a la base y el log de evento a insertar.
        """
        c= Consultas()
        cursor= conexion.cursor()
        cursor.execute(c.insertLogEvento(), (idTipoLog, idDispositivo, idMensaje, fecha))
        cursor.close()  
        conexion.commit()
        cursor= conexion.cursor()
        cursor.execute(c.selectUltimoLogEvento())
        resultado= cursor.fetchone()
        idLogEvento= resultado[0]
        cursor.close()  
        return idLogEvento
