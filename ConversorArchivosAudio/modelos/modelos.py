import datetime 
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
db = SQLAlchemy()
   
class Response(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    message = db.Column(db.String(500))
    Succeeded = db.Column(db.Boolean, default=False, nullable=False)
    errors = db.Column(db.ARRAY(db.String(5000)))
    Estado = db.Column(db.String(50))
    hora_inicio = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    hora_fin = db.Column(db.DateTime)

class ResponseSchema(SQLAlchemyAutoSchema):
    class Meta:
        model= Response
        load_instance = True
        exclude = ('id',)


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(50), unique = True)
    username = db.Column(db.String(100), unique = True)
    password = db.Column(db.String(20))
    # tereas = db.relationship('Tareas', cascade='all, delete, delete-orphan')


class UsuarioSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario
        include_relationships = True
        load_instance = True
        exclude = ('password',)