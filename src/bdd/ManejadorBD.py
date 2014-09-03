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
            sensor= Sensor(idDispositivo, nombre, modelo, nroPuerto, activoSistema, formulaConversion, tipoPuerto)
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
            actuador= Actuador(idDispositivo, nombre, modelo, nroPuerto, activoSistema, estado, tipoActuador, tipoPuerto)
            lista.append(actuador)
        return None
    
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
            self.__cargarPlacasAuxiliares(l, conexion, idDispositivo)
            placaAuxiliar= PlacaAuxiliar(idDispositivo, nombre, modelo, nroPuerto, activoSistema, nroSerie, tipoPlaca, l)
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
        #3. obtener lista placas auxiliares
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
            activoSistema= fila[3]
            factor= Factor(idFactor, nombre, unidad, None, activoSistema)
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
            activoSistema= fila[3]
            grupo= GrupoActuadores(idGrupoActuador, estado, nombre, None, activoSistema)
            lista.append(grupo)
        cursor.close()
        return lista
        
    def obtenerListaIdActuadoresGrupo(self, conexion, idGrupo):
        """
        Devuelve la lista de id de dispositivos sensores pertenecientes al factor pasado
        como parámetro
        """
        lista= list()
        c= Consultas()
        cursor= conexion.cursor()
        cursor.execute(c.selectIdActuadoresGrupo(), (idGrupo,))
        for fila in cursor:
            idActuador= fila[0]
            lista.append(idActuador)
        cursor.close()
        return lista
        
    
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
    
    def insertarSensor(self, conexion, sensor):
        """
        Inserta un sensor en la base de datos, recibe como parámetros la conexión a la base y el sensor a insertar.
        """
        return None
    
    def insertarActuador(self, conexion, actuador):
        """
        Inserta un actuador en la base de datos, recibe como parámetros la conexión a la base y el actuador a insertar.
        """
        return None
    
    def cambiarEstadoPlaca(self, conexion, estado ):
        """
        Actualiza el estado del sistema.
        Estos puede ser: I=Inactivo, C=Configuración, M=Manual o A=Automático
        """
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
    
    def insertarPlacaAuxiliar(self, conexion, placaAuxiliar):
        """
        Inserta una placa auxiliar en la base de datos.
        Recibe como parámetros la conexión a la base y la placa auxiliar a insertar.
        """
        return None
    
    def existePlacaAuxiliar(self, conexion, idActuador):
        """
        Consulta si existe actuador en la base de datos con el identificador de dispositivo pasado como parámetro.
        Recibe la conexión a la base de datos y el identificador de dispositivo correspondiente al actuador
        Devuelve un boolean.
        """
        return None
    
    def eliminadoLogicoSensor(self, conexion, idSensor):
        """
        Elimina lógicamente un sensor del sistema, esta operación consiste en cambiar su atributo activoSistema.
        Recibe como parámetros la conexión a la base de datos y el id del dispositivo sensor a eliminar.
        """
        return None
    
    def eliminadoLogicoActuador(self, conexion, idActuador):
        """
        Elimina lógicamente un actuador del sistema, esta operación consiste en cambiar su atributo activoSistema.
        Recibe como parámetros la conexión a la base de datos y el id del dispositivo actuador a eliminar.
        """
        return None
    
    def eliminadoLogicoPlacaAuxiliar(self, conexion, idPlacaAuxiliar):
        """
        Elimina lógicamente una placa auxiliar del sistema, esta operación consiste en cambiar su atributo activoSistema.
        Recibe como parámetros la conexión a la base de datos y el id del dispositivo placa auxiliar a eliminar.
        """
        return None
    
    def insertarLecturaSensor(self, conexion, resultadoLectura):
        """
        Inserta en base de datos una lectura de un sensor.
        Recibe como parámetros la conexión a la base y un objeto resultado lectura
        """
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
        return None
    
    def insertarAccionActuador(self, conexion, resultadoAccion):
        """
        Inserta en la base de datos una acción disparada sobre un actuador.
        Recibe como parámetros la conexión a la base y el resultado de la acción.
        """
        return None
    
    def insertarFactor(self, conexion, factor):
        """
        Inserta en la base de datos un factor pasado como parámetro.
        Recibe como parámetros la conexión a la base y el factor a insertar
        """
        return None
    
    def eliminadoLogicoFactor(self, conexion, idFactor):
        """
        Elimina lógicamente un factor del sistema, esta operación consiste en cambiar su atributo activoSistema.
        Recibe como parámetros la conexión a la base de datos y el id del factor a eliminar.
        """
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
    
    def insertarGrupoActuadores(self, conexion, grupoActuadores):
        """
        Inserta en la base de datos un grupo de actuadores pasado como parámetro.
        Recibe como parámetros la conexión a la base y el grupo de actuadores a insertar.
        """
        return None
    
    def eliminadoLogicoGrupoActuadores(self, conexion, idGrupoActuadores):
        """
        Elimina lógicamente un grupo de actuadores del sistema, esta operación consiste en cambiar su atributo activoSistema.
        Recibe como parámetros la conexión a la base de datos y el id del grupo de actuadores a eliminar.
        """
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
    
    def insertarNivelPerfil(self, conexion, nivelSeveridad, perfilActivacion):
        """
        Inserta en la base de datos el nivel de severidad pasado como parámetro y su perfil de activación asociado.
        Recibe como parámetros la conexión a la base, el nivel de severidad y el perfil de activación a insertar.
        """
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
        return None
    
    def insertarLogEvento (self, conexion, logEvento):
        """
        Inserta en la base de datos el log de evento pasado como parámetro.
        Recibe como parámetros la conexión a la base y el log de evento a insertar.
        """
        return None