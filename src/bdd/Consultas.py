# -*- encoding: utf-8 -*-
class Consultas(object):
    """
    Clase que se utiliza para centralizar todos los Strings de consultas a la base de datos,
    necesarios para persistir y recuperar las estructuras utilizadas en el sistema.
    """


    def __init__(self):
        """
        Contructor de la clase Consultas, no recibe parámetros.
        """
        
    def selectEstadoPlaca(self):
        """
        Devuelve la consulta para obtener el estado de la placa como un String
        """
        consulta="select estadoPlaca from parametros"
        return consulta
    
    def selectNroSeriePlaca(self):
        """
        Devuelve la consulta para obtener el estado de la placa como un String
        """
        consulta="select nroSeriePlaca from parametros"
        return consulta
    
    def selectPeriodicidadLecturaPlaca(self):
        """
        Devuelve la consulta para obtener el estado de la placa como un String
        """
        consulta="select periodicidadLecturas from parametros"
        return consulta
    
    def selectPeriodicidadNivelesPlaca(self):
        """
        Devuelve la consulta para obtener el estado de la placa como un String
        """
        consulta="select periodicidadNiveles from parametros"
        return consulta
    
    def selectSensoresActivosPlacaPadre(self):
        consulta= """select d.idDispositivo, d.nombre, d.modelo, d.nroPuerto, d.activoSistema, s.formulaConversion, s.idTipoPuerto
                     from sensores s, dispositivos d
                     where s.idDispositivo = d.idDispositivo
                        and s.idPlacaPadre is Null
                        and d.activoSistema = 'S'"""
        return consulta
    
    def selectSensoresActivosPlacaAux(self):
        consulta= """select d.idDispositivo, d.nombre, d.modelo, d.nroPuerto, d.activoSistema, s.formulaConversion, s.idTipoPuerto
                     from sensores s, dispositivos d
                     where s.idDispositivo = d.idDispositivo
                        and s.idPlacaPadre = ?
                        and d.activoSistema = 'S'"""
        return consulta
    
    def selectTipoPuerto(self):
        consulta= """select nombre
                     from tipoPuertos
                     where idTipoPuerto = ?"""
        return consulta

    
    def selectActuadoresActivosPlacaPadre(self):
        consulta="""select d.idDispositivo, d.nombre, d.modelo, d.nroPuerto, d.activoSistema, a.estado, a.idTipoPuerto, a.idTipoActuador
                    from actuadores a, dispositivos d
                    where a.idDispositivo = d.idDispositivo
                    and a.idPlacaPadre is Null
                    and d.activoSistema = 'S'"""
        return consulta
    
    def selectActuadoresAvanceActivosPlacaPadre(self):
        consulta="""select d.idDispositivo, d.nombre, d.modelo, d.nroPuerto, d.activoSistema, a.posicion, a.idTipoPuerto, a.idTipoActuador, a.nroPuertoRetroceso,
                    a.idTipoPuertoRetroceso, a.tiempoEntrePosiciones
                    from actuadoresAvance a, dispositivos d
                    where a.idDispositivo = d.idDispositivo
                    and a.idPlacaPadre is Null
                    and d.activoSistema = 'S'"""
        return consulta
    
    def selectActuadoresActivosPlacaAux(self):
        consulta="""select d.idDispositivo, d.nombre, d.modelo, d.nroPuerto, d.activoSistema, a.estado, a.idTipoPuerto, a.idTipoActuador
                    from actuadores a, dispositivos d
                    where a.idDispositivo = d.idDispositivo
                    and a.idPlacaPadre = ?
                    and d.activoSistema = 'S'"""
        return consulta
    
    def selectActuadoresAvanceActivosPlacaAux(self):
        consulta="""select d.idDispositivo, d.nombre, d.modelo, d.nroPuerto, d.activoSistema, a.posicion, a.idTipoPuerto, a.idTipoActuador, a.nroPuertoRetroceso,
                    a.idTipoPuertoRetroceso, a.tiempoEntrePosiciones
                    from actuadoresAvance a, dispositivos d
                    where a.idDispositivo = d.idDispositivo
                    and a.idPlacaPadre = ?
                    and d.activoSistema = 'S'"""
        return consulta
    
    def selectTipoActuador(self):
        consulta= """select nombre
                     from tipoActuadores
                     where idTipoActuador = ?"""
        return consulta
    
    def selectPosicionesActuadorAvance(self):
        consulta= """select posicion, descripcion, valor
                    from posiciones
                    where idActuadorAvance = ?"""
        return consulta
    
    def selectSensoresPosicion(self):
        consulta= """select idSensorAvance
                    from sensoresPosicion
                    where idActuadorAvance = ?
                        and posicion= ?"""
        return consulta

    
    def selectPlacasAuxiliaresActivasPlacaPadre(self):
        consulta="""select d.idDispositivo, d.nombre, d.modelo, d.nroPuerto, d.activoSistema, p.nroSerie, p.idTipoPlaca
                    from placasAuxiliares p, dispositivos d
                    where p.idDispositivo = d.idDispositivo
                    and p.idPlacaPadre is Null
                    and d.activoSistema = 'S'"""
        return consulta
    
    def selectPlacasAuxiliaresActivasPlacaAux(self):
        consulta="""select d.idDispositivo, d.nombre, d.modelo, d.nroPuerto, d.activoSistema, p.nroSerie, p.idTipoPlaca
                    from placasAuxiliares p, dispositivos d
                    where p.idDispositivo = d.idDispositivo
                    and p.idPlacaPadre = ?
                    and d.activoSistema = 'S'"""
        return consulta
    
    def selectGruposActuadoresActivos(self):
        consulta= """select idGrupoActuadores, estado, nombre, deAvance, activoSistema
                    from gruposActuadores
                    where activoSistema = 'S'"""
        return consulta
    
    def selectTipoPlaca(self):
        consulta= """select nombre
                    from tipoPlacas
                    where idTipoPlaca = ?"""
        return consulta
    
        
    def selectHostWS(self):
        return None
    
    def selectPuertoWS(self):
        return None
    
    def selectExisteSensor(self):
        return None
    
    def selectExisteActuador(self):
        return None
    
    def selectExistePlacaAuxiliar(self):
        return None
    
    def selectLecturasPorFecha(self):
        return None
    
    def selectLecturasPorCantidad(self):
        consulta= """select valor
                    from lecturasFactores
                    where idFactor= ?
                    order by fecha desc
                    limit ?"""
        return consulta
    
    def selectFactorId(self):
        return None
    
    def selectFactorNombre(self):
        return None
    
    def selectFactores(self):
        consulta="""select idFactor, nombre, unidad, valorMin, valorMax, umbral, activoSistema
                    from factores
                    where activoSistema= 'S'"""
        return consulta
        
    def selectIdSensoresFactor(self):
        consulta="""select idDispositivo
                    from sensores
                    where idFactor = ?"""
        return consulta
    
    def selectIdActuadoresGrupo(self):
        consulta="""select idDispositivo
                    from actuadores
                    where idGrupoActuadores = ?"""
        return consulta

    def selectIdActuadoresAvanceGrupo(self):
        consulta="""select idDispositivo
                    from actuadoresAvance
                    where idGrupoActuadores = ?"""
        return consulta
    
    def selectExisteNivelSeveridad(self):
        return None
    
    def selectObtenerNivelesSeveridad(self):
        consulta= "select idNivel, nombre, idFactor, prioridad, rangoMinimo, rangoMaximo, idPerfilActivacion, activoSistema from nivelesSeveridad where activoSistema = 'S'"
        return consulta
    
    def selectIdGruposActuadoresEstadosActivosPerfil(self):
        consulta="select idGrupoActuadores, estado from perfilesActivacion where idPerfilActivacion = ? and activoSistema = 'S'"
        return consulta
    
    def selectMensaje(self):
        consulta= """select m.idMensaje, t.nombre, m.texto
                    from mensajes m, tipoMensajes t
                    where m.idTipoMensaje = t.idTipoMensaje and m.idMensaje = ? """
        return consulta
    
    def selectUltimoFactor(self):
        consulta= "select max(idFactor) from factores"
        return consulta
    
    def selectUltimoTipoPlaca(self):
        consulta= "select max(idTipoPlaca) from tipoPlacas"
        return consulta
    
    def selectUltimoTipoActuador(self):
        consulta= "select max(idTipoActuador) from tipoActuadores"
        return consulta
    
    def selectUltimoDispositivo(self):
        consulta= "select max(idDispositivo) from dispositivos"
        return consulta
    
    def selectUltimoGrupoActuadores(self):
        consulta= "select max(idGrupoActuadores) from gruposActuadores"
        return consulta
    
    def selectUltimoNivelSeveridad(self):
        consulta= "select max(idNivel) from nivelesSeveridad"
        return consulta
    
    
    def insertActuador(self):
        consulta= """insert into actuadores (idDispositivo, estado, idTipoPuerto, idTipoActuador, idPlacaPadre, idGrupoActuadores, fechaAlta)
                    values (?, 'A', ?, ?, ?, ?, datetime('now', 'localtime'))"""
        return consulta
    
    def insertPosicion(self):
        consulta= "insert into posiciones (idActuadorAvance, posicion, descripcion, valor) values (?, ?, ?, ?)"
        return consulta
    
    def insertSensorPosicion(self):
        consulta= "insert into sensoresPosicion (idSensorAvance, idActuadorAvance, posicion) values (?, ?, ?)"
        return consulta
    
    def insertActuadorAvance(self):
        consulta= """insert into actuadoresAvance (idDispositivo, posicion, idTipoPuerto, idTipoActuador, idPlacaPadre, nroPuertoRetroceso, idTipoPuertoRetroceso, tiempoEntrePosiciones, idGrupoActuadores, fechaAlta)
                    values (?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now', 'localtime'))"""
        return consulta
    
    def insertSensor(self):
        consulta="""insert into sensores (idDispositivo, formulaConversion, idTipoPuerto, idPlacaPadre, idFactor, fechaAlta)
                    values (?, ?, ?, ?, ?, datetime('now', 'localtime'))"""
        return consulta
    
    def insertTipoPlaca(self):
        consulta="insert into tipoPLacas (nombre) values (?)"
        return consulta
    
    def insertTipoActuador(self):
        consulta="insert into tipoActuadores (nombre) values (?)"
        return consulta
    
    def insertFactor(self):
        consulta= """insert into factores (nombre, unidad, valorMin, valorMax, umbral, activoSistema)
                        values (?, ?, ?, ?, ?, ?)"""
        return consulta
    
    def insertDispositivo(self):
        consulta= """insert into dispositivos (nombre, modelo, nroPuerto, activoSistema) 
                        values (?, ?, ?, ?)"""
        return consulta
    
    def insertPlacaAuxiliar(self):
        consulta= "insert into placasAuxiliares (idDispositivo, nroSerie, idTipoPlaca, idPlacaPadre, fechaAlta) values (?, ?, ?, ?, datetime('now', 'localtime'))"
        return consulta
    
    def insertLecturaSensor(self):
        consulta="insert into lecturas (idDispositivo, fecha, valor) values (?, datetime('now', 'localtime'), ?)"
        return consulta
    
    def insertLecturaFactor(self):
        consulta="insert into lecturasFactores (idFactor, fecha, valor) values (?, ?, ?)"
        return consulta
    
    def insertAccionActuador(self):
        consulta="insert into acciones (idDispositivo, fecha, tipoAccion) values (?, datetime('now', 'localtime'), ?)"
        return consulta
    
    def insertGrupoActuadores(self):
        consulta= "insert into gruposActuadores (estado, nombre, deAvance, activoSistema) values ('A', ?, 'N', 'S')"
        return consulta
    
    def insertGrupoActuadoresAvance(self):
        consulta= "insert into gruposActuadores (estado, nombre, deAvance, activoSistema) values ('1', ?, 'S', 'S')"
        return consulta
    
    def insertNivelSeveridad(self):
        consulta= """insert into nivelesSeveridad (nombre, idFactor, prioridad, rangoMinimo, rangoMaximo, activoSistema)
                        values (?, ?, ?, ?, ?, 'S')"""
        return consulta
    
    def insertPerfilActivacion(self):
        consulta= "insert into perfilesActivacion (idPerfilActivacion, idGrupoActuadores, estado, activoSistema) values (?, ?, ?, 'S')"
        return consulta
    
    def insertLogEvento(self):
        return None
    
    def updateEstadoActuador(self):
        consulta = "update actuadores set estado = ? where idDispositivo= ?"
        return consulta
    
    def updateEstadoGrupoActuadores(self):
        consulta = "update gruposactuadores set estado = ? where idGrupoActuadores= ?"
        return consulta
    
    def updateIdPerfilActivacion(self):
        consulta = "update nivelesSeveridad set idPerfilActivacion = ? where idNivel= ?"
        return consulta
    
    def updateEstadoPlaca(self):
        consulta= "update parametros set estadoPlaca=?"
        return consulta
    
    def updatePosicionActuadorAvance(self):
        consulta= "update actuadoresAvance set posicion = ? where idDispositivo = ?"
        return consulta
    
    def updateActivoSistemaDispositivo(self):
        consulta= "update dispositivos set activoSistema = 'N' where idDispositivo = ?"
        return consulta
    
    def updateActivoSistemaFactor(self):
        consulta= "update factores set activoSistema = 'N' where idFactor = ?"
        return consulta
    
    def updateActivoSistemaGrupoActuadores(self):
        consulta= "update gruposActuadores set activoSistema = 'N' where idGrupoActuadores = ?"
        return consulta
    
    def updateActivoSistemaNivelSeveridad(self):
        consulta= "update nivelesSeveridad set activoSistema = 'N' where idNivel = ?"
        return consulta
    
    def updateActivoSistemaPerfilActivacion(self):
        consulta= "update perfilesActivacion set activoSistema = 'N' where idPerfilActivacion = ? and idGrupoActuadores = ?"
        return consulta
        