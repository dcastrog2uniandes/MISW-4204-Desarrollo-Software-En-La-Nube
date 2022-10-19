from modelos.modelos import db, Tarea, FileStatus
class ActualizarEstado:
    def actualizarEstadoTarea(self, tarea_json):
        if tarea_json['status'] == FileStatus.PROCESSED.name:
            tarea = Tarea.query.filter( Tarea.id == int(tarea_json['id'])).first()
            if tarea:
                tarea.status = FileStatus.PROCESSED.name
                db.session.commit()