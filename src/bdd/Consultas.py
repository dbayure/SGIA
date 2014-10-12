# -*- encoding: utf-8 -*-
class Consultas(object):
    """
    Clase que se utiliza para centralizar todos los Strings de consultas a la base de datos,
    necesarios para persistir y recuperar las estructuras utilizadas en el sistema.
    """


    def __init__(self):
        """Contructor de la clase Consultas, no recibe parámetros."""
        
    def selectEstadoPlaca(self):
        """Devuelve la consulta para obtener el estado de la placa."""
        consulta="select estadoPlaca from parametros"
        return consulta
    
    def selectNroSeriePlaca(self):
        """Devuelve la consulta para obtener el número de serie de la placa."""
        consulta="select nroSeriePlaca from parametros"
        return consulta
    
    def selectEstadoAlertaSistema(self):
        """Devuelve la consulta para obtener el estado de alerta del sistema."""
        consulta="select estadoAlerta from parametros"
        return consulta
    
    def selectCantidadDispositivosEnAlerta(self):
        """Devuelve la consulta para obtener la cantidad de dispositivos en estado de alerta"""
        consulta= "select count(*) from dispositivos where activoSistema = 'S' and estadoAlerta = 'S'"
        return consulta
    
    def selectPeriodicidadLecturaPlaca(self):
        """Devuelve la consulta para obtener la periodicidad de lecturas de la placa."""
        consulta="select periodicidadLecturas from parametros"
        return consulta
    
    def selectPeriodicidadNivelesPlaca(self):
        """Devuelve la consulta para obtener la periodicidad de procesado de los niveles de severidad de la placa."""
        consulta="select periodicidadNiveles from parametros"
        return consulta
    
    def selectSensoresActivosPlacaPadre(self):
        """Devuelve la consulta para obtener la lista de sensores activos conectados directamente a la placa controladora."""
        consulta= """select d.idDispositivo, d.nombre, d.modelo, d.nroPuerto, d.activoSistema, d.estadoAlerta, s.formulaConversion, s.idTipoPuerto
                     from sensores s, dispositivos d
                     where s.idDispositivo = d.idDispositivo
                        and s.idPlacaPadre is Null
                        and d.activoSistema = 'S'"""
        return consulta
    
    def selectSensoresActivosPlacaAux(self):
        """Devuelve la consulta para obtener la lista de sensores activos conectados directamente a una placa auxiliar."""
        consulta= """select d.idDispositivo, d.nombre, d.modelo, d.nroPuerto, d.activoSistema, d.estadoAlerta, s.formulaConversion, s.idTipoPuerto
                     from sensores s, dispositivos d
                     where s.idDispositivo = d.idDispositivo
                        and s.idPlacaPadre = ?
                        and d.activoSistema = 'S'"""
        return consulta
    
    def selectTipoPuerto(self):
        """Devuelve la consulta para obtener el nombre de un tipo puerto dado su idTipoPuerto"""
        consulta= """select nombre
                     from tipoPuertos
                     where idTipoPuerto = ?"""
        return consulta
    
    def selectActuadoresActivosPlacaPadre(self):
        """Devuelve la consulta para obtener la lista de actuadores conectados directamente a la placa controladora."""
        consulta="""select d.idDispositivo, d.nombre, d.modelo, d.nroPuerto, d.activoSistema, d.estadoAlerta, a.estado, a.idTipoPuerto, a.idTipoActuador
                    from actuadores a, dispositivos d
                    where a.idDispositivo = d.idDispositivo
                    and a.idPlacaPadre is Null
                    and d.activoSistema = 'S'"""
        return consulta
    
    def selectActuadoresAvanceActivosPlacaPadre(self):
        """Devuelve la consulta para obtener la lista de actuadores de avance conectados directamente a la placa controladora."""
        consulta="""select d.idDispositivo, d.nombre, d.modelo, d.nroPuerto, d.activoSistema, d.estadoAlerta, a.posicion, a.idTipoPuerto, a.idTipoActuador, a.nroPuertoRetroceso,
                    a.idTipoPuertoRetroceso, a.tiempoEntrePosiciones
                    from actuadoresAvance a, dispositivos d
                    where a.idDispositivo = d.idDispositivo
                    and a.idPlacaPadre is Null
                    and d.activoSistema = 'S'"""
        return consulta
    
    def selectActuadoresActivosPlacaAux(self):
        """Devuelve la consulta para obtener la lista de actuadores conectados directamente a una placa auxiliar."""
        consulta="""select d.idDispositivo, d.nombre, d.modelo, d.nroPuerto, d.activoSistema, d.estadoAlerta, a.estado, a.idTipoPuerto, a.idTipoActuador
                    from actuadores a, dispositivos d
                    where a.idDispositivo = d.idDispositivo
                    and a.idPlacaPadre = ?
                    and d.activoSistema = 'S'"""
        return consulta
    
    def selectActuadoresAvanceActivosPlacaAux(self):
        """Devuelve la consulta para obtener la lista de actuadores de avance conectados directamente a una placa auxiliar."""
        consulta="""select d.idDispositivo, d.nombre, d.modelo, d.nroPuerto, d.activoSistema, d.estadoAlerta, a.posicion, a.idTipoPuerto, a.idTipoActuador, a.nroPuertoRetroceso,
                    a.idTipoPuertoRetroceso, a.tiempoEntrePosiciones
                    from actuadoresAvance a, dispositivos d
                    where a.idDispositivo = d.idDispositivo
                    and a.idPlacaPadre = ?
                    and d.activoSistema = 'S'"""
        return consulta
    
    def selectTipoActuador(self):
        """Devuelve la consulta para obtener el nombre de un tipoActuador dado su idTipoActuador"""
        consulta= """select nombre
                     from tipoActuadores
                     where idTipoActuador = ?"""
        return consulta
    
    def selectPosicionesActuadorAvance(self):
        """Devuelve la consulta para obtener la lista de posiciones de un actuador de avance dado el idActuadorAvance."""
        consulta= """select posicion, descripcion, valor
                    from posiciones
                    where idActuadorAvance = ?"""
        return consulta
    
    def selectSensoresPosicion(self):
        """Devuelve la lista de sensores correspondientes a una posición, dados un idActuadorAvance y el número de posición."""
        consulta= """select idSensorAvance
                    from sensoresPosicion
                    where idActuadorAvance = ?
                        and posicion= ?"""
        return consulta

    
    def selectPlacasAuxiliaresActivasPlacaPadre(self):
        """Devuelve la consulta para obtener la lista de placas auxiliares activas conectadas directamente a la placa controladora."""
        consulta="""select d.idDispositivo, d.nombre, d.modelo, d.nroPuerto, d.activoSistema, d.estadoAlerta,  p.nroSerie, p.idTipoPlaca
                    from placasAuxiliares p, dispositivos d
                    where p.idDispositivo = d.idDispositivo
                    and p.idPlacaPadre is Null
                    and d.activoSistema = 'S'"""
        return consulta
    
    def selectPlacasAuxiliaresActivasPlacaAux(self):
        """Devuelve la consulta para obtener la lista de placas auxiliares activas conectadas directamente a a una placa auxiliar, dado un idPlacaPadre."""
        consulta="""select d.idDispositivo, d.nombre, d.modelo, d.nroPuerto, d.activoSistema, d.estadoAlerta, p.nroSerie, p.idTipoPlaca
                    from placasAuxiliares p, dispositivos d
                    where p.idDispositivo = d.idDispositivo
                    and p.idPlacaPadre = ?
                    and d.activoSistema = 'S'"""
        return consulta
    
    def selectGruposActuadoresActivos(self):
        """Devuelve la consulta para obtener la lista de grupos de actuadores activos en el sistema"""
        consulta= """select idGrupoActuadores, estado, nombre, deAvance, activoSistema
                    from gruposActuadores
                    where activoSistema = 'S'"""
        return consulta
    
    def selectTipoPlaca(self):
        """Devuelve la consulta para obtener el nombre de un tipo de placa auxiliar dado un idTipoPlaca"""
        consulta= """select nombre
                    from tipoPlacas
                    where idTipoPlaca = ?"""
        return consulta
    
    def selectHostPuertoWS(self):
        """Devuelve la consulta para obtener el host y puerto en el que se van a publicar los servicios web brindados por la placa controladora"""
        consulta="select hostWS, puertoWS from parametros"
        return consulta
    
    def selectHostPuertoWS_SMS(self):
        """Devuelve la consulta para obtener el host y puerto en el que está publicado el servicio web para envío de SMS"""
        consulta="select hostWS_SMS, puertoWS_SMS from parametros"
        return consulta
    
    def selectHostPuertoWS_Centralizadora(self):
        """Devuelve la consulta para obtener el host y puerto en el que están publicados los servicios web brindados por la aplicación centralizadora."""
        consulta="select hostWS_Centralizadora, puertoWS_Centralizadora from parametros"
        return consulta

    def selectLecturasPorCantidad(self):
        """Devuelve la consulta para obtener las últimas n lecturas de un factor, dados un idFactor y la cantidad n de lecturas que se pretende recuperar"""
        consulta= """select valor
                    from lecturasFactores
                    where idFactor= ?
                    order by fecha desc
                    limit ?"""
        return consulta
    
    def selectFactores(self):
        """Devuelve la consulta para obtener la lista de factores activos en el sistema."""
        consulta="""select idFactor, nombre, unidad, valorMin, valorMax, umbral, activoSistema
                    from factores
                    where activoSistema= 'S'"""
        return consulta
        
    def selectIdSensoresFactor(self):
        """Devuelve la consulta para obtener la lista de ids de sensores asociados a un factor, dado un idFactor."""
        consulta="""select idDispositivo
                    from sensores
                    where idFactor = ?"""
        return consulta
    
    def selectIdActuadoresGrupo(self):
        """Devuelve la consulta para obtener la lista de ids de actuadores asociados a un grupo de actuadores, dado un idGrupoActuadores."""
        consulta="""select idDispositivo
                    from actuadores
                    where idGrupoActuadores = ?"""
        return consulta

    def selectIdActuadoresAvanceGrupo(self):
        """Devuelve la consulta para obtener la lista de ids de actuadores de avance asociados a un grupo de actuadores, dado un idGrupoActuadores."""
        consulta="""select idDispositivo
                    from actuadoresAvance
                    where idGrupoActuadores = ?"""
        return consulta
    
    def selectObtenerNivelesSeveridad(self):
        """Devuelve la consulta para obtener la lista de niveles de severidad activos en el sistema."""
        consulta= "select idNivel, nombre, idFactor, prioridad, rangoMinimo, rangoMaximo, idPerfilActivacion, activoSistema from nivelesSeveridad where activoSistema = 'S'"
        return consulta
    
    def selectIdGruposActuadoresEstadosActivosPerfil(self):
        """Devuelve la consulta para obtener la lista de tuplas compuestas por un id de grupo actuador y un estado asignado a este, activas en el sistema, dado un idPerfilActivación."""
        consulta="select idGrupoActuadores, estado from perfilesActivacion where idPerfilActivacion = ? and activoSistema = 'S'"
        return consulta
    
    def selectMensaje(self):
        """Devuelve la consulta para obtener un mensaje, dado un idMensaje."""
        consulta= """select m.idMensaje, t.nombre, m.texto
                    from mensajes m, tipoMensajes t
                    where m.idTipoMensaje = t.idTipoMensaje and m.idMensaje = ? """
        return consulta
    
    def selectTipoLogEventos(self):
        """Devuelve la consulta para obtener un tipo de log de eventos, dado un idTipoLogEventos"""
        consulta= "select idTipoLogEventos, nombre, enviarSMS, enviarMAIL from tipoLogEventos where idTipoLogEventos = ?"
        return consulta
    
    def selectUltimoFactor(self):
        """Devuelve la consulta para obtener el id del último factor agregado al sistema."""
        consulta= "select max(idFactor) from factores"
        return consulta
    
    def selectListaDestinatarios(self):
        """Devuelve la consulta para obtener la lista de destinatarios asociados a un tipo de log de eventos, dado un idTipoLogEvento"""
        consulta= """select d.idDestinatario, d.nombre, d.celular, d.mail, d.horaMin, d.horaMax
                    from destinatarios d, destinatariosTiposLog t
                    where d.idDestinatario = t.idDestinatario
                        and t.idTipoLogEvento= ?"""
        return consulta
    
    def selectUltimoTipoPlaca(self):
        """Devuelve la consulta para obtener el id del último tipoPlaca agregado al sistema."""
        consulta= "select max(idTipoPlaca) from tipoPlacas"
        return consulta
    
    def selectUltimoTipoActuador(self):
        """Devuelve la consulta para obtener el id del último tipo de actuador agregado al sistema."""
        consulta= "select max(idTipoActuador) from tipoActuadores"
        return consulta
    
    def selectUltimoDispositivo(self):
        """Devuelve la consulta para obtener el id del último dispositivo agregado al sistema."""
        consulta= "select max(idDispositivo) from dispositivos"
        return consulta
    
    def selectUltimoGrupoActuadores(self):
        """Devuelve la consulta para obtener el id del último grupo de actuadores agregado al sistema."""
        consulta= "select max(idGrupoActuadores) from gruposActuadores"
        return consulta
    
    def selectUltimoNivelSeveridad(self):
        """Devuelve la consulta para obtener el id del último nivel de severidad agregado al sistema."""
        consulta= "select max(idNivel) from nivelesSeveridad"
        return consulta
    
    def selectUltimoLogEvento(self):
        """Devuelve la consulta para obtener el id del último log de evento agregado al sistema."""
        consulta= "select max(idLogEvento) from logEventos"
        return consulta
    
    def insertActuador(self):
        """Devuelve la consulta para insertar un actuador al sistema.
        Se deben sustituir los siguientes parámetros: idDispositivo, idTipoPuerto, idTipoActuador, idPlacaPadre, idGrupoActuadores"""
        consulta= """insert into actuadores (idDispositivo, estado, idTipoPuerto, idTipoActuador, idPlacaPadre, idGrupoActuadores, fechaAlta)
                    values (?, 'A', ?, ?, ?, ?, datetime('now', 'localtime'))"""
        return consulta
    
    def insertPosicion(self):
        """Devuelve la consulta para insertar una posición al sistema.
        Se deben sustituir los siguientes parámetros: idActuadorAvance, posicion, descripcion, valor"""
        consulta= "insert into posiciones (idActuadorAvance, posicion, descripcion, valor) values (?, ?, ?, ?)"
        return consulta
    
    def insertSensorPosicion(self):
        """Devuelve la consulta para insertar una asociación entre un sensor y una posición existentes.
        Se deben sustituir los siguientes parámetros: idSensorAvance, idActuadorAvance, posicion"""
        consulta= "insert into sensoresPosicion (idSensorAvance, idActuadorAvance, posicion) values (?, ?, ?)"
        return consulta
    
    def insertActuadorAvance(self):
        """Devuelve la consulta para insertar un actuador de avance al sistema.
        Se deben sustituir los siguientes parámetros: idDispositivo, posicion, idTipoPuerto, idTipoActuador, idPlacaPadre, nroPuertoRetroceso, idTipoPuertoRetroceso, tiempoEntrePosiciones, idGrupoActuadores"""
        consulta= """insert into actuadoresAvance (idDispositivo, posicion, idTipoPuerto, idTipoActuador, idPlacaPadre, nroPuertoRetroceso, idTipoPuertoRetroceso, tiempoEntrePosiciones, idGrupoActuadores, fechaAlta)
                    values (?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now', 'localtime'))"""
        return consulta
    
    def insertSensor(self):
        """Devuelve la consulta para insertar un sensor al sistema.
        Se deben sustituir los siguientes parámetros: idDispositivo, formulaConversion, idTipoPuerto, idPlacaPadre, idFactor"""
        consulta="""insert into sensores (idDispositivo, formulaConversion, idTipoPuerto, idPlacaPadre, idFactor, fechaAlta)
                    values (?, ?, ?, ?, ?, datetime('now', 'localtime'))"""
        return consulta
    
    def insertTipoPlaca(self):
        """Devuelve la consulta para insertar un tipo de placa auxiliar al sistema, se debe sustituir el parámetro nombre"""
        consulta="insert into tipoPLacas (nombre) values (?)"
        return consulta
    
    def insertTipoActuador(self):
        """Devuelve la consulta para insertar un tipo de actuador auxiliar al sistema, se debe sustituir el parámetro nombre"""
        consulta="insert into tipoActuadores (nombre) values (?)"
        return consulta
    
    def insertFactor(self):
        """Devuelve la consulta para insertar un factor al sistema.
        Se deben sustituir los parámetros: nombre, unidad, valorMin, valorMax, umbral, activoSistema"""
        consulta= """insert into factores (nombre, unidad, valorMin, valorMax, umbral, activoSistema)
                        values (?, ?, ?, ?, ?, ?)"""
        return consulta
    
    def insertDispositivo(self):
        """Devuelve la consulta para insertar un dispositivo al sistema.
        Se deben sustituir los siguientes parámetros: nombre, modelo, nroPuerto, activoSistema"""
        consulta= """insert into dispositivos (nombre, modelo, nroPuerto, activoSistema, estadoAlerta) 
                        values (?, ?, ?, ?, 'N')"""
        return consulta
    
    def insertPlacaAuxiliar(self):
        """Devuelve la consulta para insertar una placa auxiliar al sistema.
        Se deben sustituir los siguientes parámetros: idDispositivo, nroSerie, idTipoPlaca, idPlacaPadre"""
        consulta= "insert into placasAuxiliares (idDispositivo, nroSerie, idTipoPlaca, idPlacaPadre, fechaAlta) values (?, ?, ?, ?, datetime('now', 'localtime'))"
        return consulta
    
    def insertLecturaSensor(self):
        """Devuelve la consulta para insertar una lectura de un sensor.
        Se deben sustituir los siguientes parámetros: idDispositivo, valor"""
        consulta="insert into lecturas (idDispositivo, fecha, valor) values (?, datetime('now', 'localtime'), ?)"
        return consulta
    
    def insertLecturaFactor(self):
        """Devuelve la consulta para insertar una lectura de un factor.
        Se deben sustituir los siguientes parámetros: idFactor, fecha, valor"""
        consulta="insert into lecturasFactores (idFactor, fecha, valor) values (?, ?, ?)"
        return consulta
    
    def insertAccionActuador(self):
        """Devuelve la consulta para insertar una acción de un actuador.
        Se deben sustituir los siguientes parámetros: idDispositivo, tipoAccion"""
        consulta="insert into acciones (idDispositivo, fecha, tipoAccion) values (?, datetime('now', 'localtime'), ?)"
        return consulta
    
    def insertGrupoActuadores(self):
        """Devuelve la consulta para insertar un grupo de actuadores al sistema. Se debe sustituir el parámetro nombre"""
        consulta= "insert into gruposActuadores (estado, nombre, deAvance, activoSistema) values ('A', ?, 'N', 'S')"
        return consulta
    
    def insertGrupoActuadoresAvance(self):
        """Devuelve la consulta para insertar un grupo de actuadores de avance al sistema. Se debe sustituir el parámetro nombre"""
        consulta= "insert into gruposActuadores (estado, nombre, deAvance, activoSistema) values ('1', ?, 'S', 'S')"
        return consulta
    
    def insertNivelSeveridad(self):
        """Devuelve la consulta para insertar un nivel de severidad al sistema.
        Se deben sustituir los siguientes parámetros: nombre, idFactor, prioridad, rangoMinimo, rangoMaximo"""
        consulta= """insert into nivelesSeveridad (nombre, idFactor, prioridad, rangoMinimo, rangoMaximo, activoSistema)
                        values (?, ?, ?, ?, ?, 'S')"""
        return consulta
    
    def insertPerfilActivacion(self):
        """Devuelve la consulta para insertar un perfil de activación al sistema.
        Se deben sustituir los siguientes parámetros: idPerfilActivacion, idGrupoActuadores, estado"""
        consulta= "insert into perfilesActivacion (idPerfilActivacion, idGrupoActuadores, estado, activoSistema) values (?, ?, ?, 'S')"
        return consulta
    
    def insertLogEvento(self):
        """Devuelve la consulta para insertar un log de eventos al sistema.
        Se deben sustituir los siguientes parámetros: idTipoLog, idDispositivo, idMensaje, fecha"""
        consulta= "insert into logEventos (idTipoLog, idDispositivo, idMensaje, fecha) values (?, ?, ?, ?)"
        return consulta
    
    def updateEstadoActuador(self):
        """Devuelve la consulta para actualizar el estado de un actuador, dados el estado y un idDispositivo"""
        consulta = "update actuadores set estado = ? where idDispositivo= ?"
        return consulta
    
    def updateEstadoGrupoActuadores(self):
        """Devuelve la consulta para actualizar el estado de un grupo de actuadores, dados el estado y un idGrupoActuadores"""
        consulta = "update gruposactuadores set estado = ? where idGrupoActuadores= ?"
        return consulta
    
    def updateIdPerfilActivacion(self):
        """Devuelve la consulta para actualizar el id de perfil de activación asociado a un nivel de severidad, dados el idPerfilActivacion e idNivel"""
        consulta = "update nivelesSeveridad set idPerfilActivacion = ? where idNivel= ?"
        return consulta
    
    def updateEstadoPlaca(self):
        """Devuelve la consulta para actualizar el estado del sistema"""
        consulta= "update parametros set estadoPlaca=?"
        return consulta
    
    def updateEstadoAlertaSistema(self):
        """Devuelve la consulta para actualizar el estado de alerta del sistema"""
        consulta= "update parametros set estadoAlerta=?"
        return consulta
    
    def updatePosicionActuadorAvance(self):
        """Devuelve la consulta para actualizar la posición de un actuador de avance, dados el número de posición y un idDispositivo"""
        consulta= "update actuadoresAvance set posicion = ? where idDispositivo = ?"
        return consulta
    
    def updateActivoSistemaDispositivo(self):
        """Devuelve la consulta para actualizar el estado activo sistema a 'N' de un dispositivo, dado su idDispositivo"""
        consulta= "update dispositivos set activoSistema = 'N' where idDispositivo = ?"
        return consulta
    
    def updateActivoSistemaFactor(self):
        """Devuelve la consulta para actualizar el estado activo sistema a 'N' de un factor, dado su idFactor"""
        consulta= "update factores set activoSistema = 'N' where idFactor = ?"
        return consulta
    
    def updateActivoSistemaGrupoActuadores(self):
        """Devuelve la consulta para actualizar el estado activo sistema a 'N' de un grupo de actuadores, dado su idGrupoActuador"""
        consulta= "update gruposActuadores set activoSistema = 'N' where idGrupoActuadores = ?"
        return consulta
    
    def updateActivoSistemaNivelSeveridad(self):
        """Devuelve la consulta para actualizar el estado activo sistema a 'N' de un nivel de severidad, dado su idNivel"""
        consulta= "update nivelesSeveridad set activoSistema = 'N' where idNivel = ?"
        return consulta
    
    def updateActivoSistemaPerfilActivacion(self):
        """Devuelve la consulta para actualizar el estado activo sistema a 'N' de una fila de un perfil de activación, dados un idPerfilActivacion e idGrupoActuadores"""
        consulta= "update perfilesActivacion set activoSistema = 'N' where idPerfilActivacion = ? and idGrupoActuadores = ?"
        return consulta
    
    def updateEstadoAlertaDispositivo(self):
        """Devuelve la consulta para actualizar el estado de alerta de un dispositivo, dados el estadoAlerta y su idDispositivo"""
        consulta= "update dispositivos set estadoAlerta = ? where idDispositivo = ?"
        return consulta
    