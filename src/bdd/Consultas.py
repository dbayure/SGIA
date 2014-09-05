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
    
    def selectActuadoresActivosPlacaAux(self):
        consulta="""select d.idDispositivo, d.nombre, d.modelo, d.nroPuerto, d.activoSistema, a.estado, a.idTipoPuerto, a.idTipoActuador
                    from actuadores a, dispositivos d
                    where a.idDispositivo = d.idDispositivo
                    and a.idPlacaPadre = ?
                    and d.activoSistema = 'S'"""
        return consulta
    
    def selectTipoActuador(self):
        consulta= """select nombre
                     from tipoActuadores
                     where idTipoActuador = ?"""
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
        consulta= """select idGrupoActuadores, estado, nombre, activoSistema
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
        return None
    
    def selectFactorId(self):
        return None
    
    def selectFactorNombre(self):
        return None
    
    def selectFactores(self):
        consulta="""select idFactor, nombre, unidad, activoSistema
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


    
    def selectExisteNivelSeveridad(self):
        return None
    
    def selectObtenerNivelesSeveridad(self):
        return None
    
    def selectObtenerPerfilActivacion(self):
        return None
    
    def selectMensaje(self):
        return None
    
    def insertActuador(self):
        return None
    
    def insertSensor(self):
        return None
    
    def insertDispositivo(self):
        return None
    
    def insertPlacaAuxiliar(self):
        return None
    
    def insertLecturaSensor(self):
        return None
    
    def insertAccionActuador(self):
        return None
    
    def insertGrupoActuadores(self):
        return None
    
    def insertNivelSeveridad(self):
        return None
    
    def insertPerfilActivacion(self):
        return None
    
    def insertLogEvento(self):
        return None
    
    def updateEstadoActuador(self):
        consulta = "update actuadores set estado = ? where idDispositivo= ?"
        return consulta
    
    def updateEstadoGrupoActuadores(self):
        consulta = "update gruposactuadores set estado = ? where idGrupoActuadores= ?"
        return consulta
    
    def updateEstadoPlaca(self):
        return None
    
    def updateActivoSistemaSensor(self):
        return None
    
    def updateActivoSistemaActuador(self):
        return None
    
    def updateActivoSistemaPlacaAuxiliar(self):
        return None
    
    def updateActivoSistemaFactor(self):
        return None
    
    def updateActivoSistemaGrupoActuadores(self):
        return None
    
    def updateActivoSistemaNivelSeveridad(self):
        return None
    
    def updateActivoSistemaPerfilActivacion(self):
        return None
        