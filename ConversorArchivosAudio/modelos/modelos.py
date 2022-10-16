import datetime
from attr import fields 
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_enum import EnumField
import enum

db = SQLAlchemy()

class Response:
    message = str()
    succeded = bool()
    errors = []
    Estado = str()
    hora_inicio = str()
    hora_fin = str()

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(50), unique = True)
    username = db.Column(db.String(100), unique = True)
    password = db.Column(db.String(20))
    tareas = db.relationship('Tarea', cascade='all, delete, delete-orphan')

class FileStatus (str, enum.Enum):
    UPLOADED = 0
    PROCESSED = 1
    
class Tarea(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    fileConvertido = db.Column(db.String(5000))
    fileOriginal = db.Column(db.String(5000))
    newFormat = db.Column(db.String(5))
    status = db.Column(db.Enum(FileStatus))
    timeStamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    usuario = db.Column(db.Integer, db.ForeignKey("usuario.id"))

class UsuarioSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario
        include_relationships = True
        load_instance = True
        exclude = ('password',)

class TareaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model= Tarea
        load_instance = True
    status = EnumField(enum=FileStatus, required=True)