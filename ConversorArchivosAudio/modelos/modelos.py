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