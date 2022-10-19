from modelos.modelos import db, Tarea, FileStatus
class ActualizarEstado:
    def actualizarEstadoTarea(self, tarea_json):
        print(tarea_json)
        if tarea_json['status'] == FileStatus.PROCESSED.name:
            print('procesando')
            tarea = Tarea.query.filter( Tarea.id == int(tarea_json['id'])).first()
            tarea.status = FileStatus.PROCESSED.name
            db.session.commit()