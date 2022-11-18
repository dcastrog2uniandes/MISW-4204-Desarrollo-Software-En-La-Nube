from flask import Flask
from modelos.modelos import db, Tarea, FileStatus
from conectarBD.conectarBD import ConectarBD

class ActualizarEstado:
    def actualizarEstadoTarea(self, tarea_json):
        app = Flask(__name__)
        conectar = ConectarBD()
        conectar.conectar(app)
        if tarea_json['status'] == FileStatus.PROCESSED.name:
            tarea = Tarea.query.filter( Tarea.id == int(tarea_json['id'])).first()
            if tarea:
                tarea.status = FileStatus.PROCESSED.name
                db.session.commit()