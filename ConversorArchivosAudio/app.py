from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api
from modelos.modelos import db
from registro.registro import Registro
from crearTarea.creartarea import CrearTarea
from obtenerTareas.obtenerTareas import ObtenerTareas
from obtenerTarea.obtenerTarea import ObtenerTarea 
from eliminarTarea.eliminarTarea import EliminarTarea
from login.login import Login
from actualizarTarea.actualizatarea import ActualizarTarea
from recuperarArchivo.recuperarArchivo import RecuperarArchivo
import os

app = Flask(__name__)

ISCONTAINER = os.environ.get('ISCONTAINER', None)
PASSWORD = os.environ.get('PASSWORD', None)
PUBLIC_IP_ADDRESS = os.environ.get('PUBLIC_IP_ADDRESS', None)
DBNAME = os.environ.get('DBNAME', None)
PROJECT_ID = os.environ.get('PROJECT_ID', None)
INSTANCE_NAME = os.environ.get('INSTANCE_NAME', None)

if ISCONTAINER is None:
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:{}@{}/{}".format(PASSWORD, PUBLIC_IP_ADDRESS, DBNAME)
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+mysqldb://root:{PASSWORD}@{PUBLIC_IP_ADDRESS}/{DBNAME}?unix_socket=/cloudsql/{PROJECT_ID}:{INSTANCE_NAME}"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= True

#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///conversorAudio.db'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['JWT_SECRET_KEY'] = 'frase-secreta'
app.config['PROPAGATE_EXCEPTIONS'] = True

app_context = app.app_context()
app_context.push()
 
db.init_app(app)
db.create_all()

cors = CORS(app)

api = Api(app)

api.add_resource(Registro, '/api/auth/signup')
api.add_resource(Login, '/api/auth/login')
api.add_resource(CrearTarea, '/api/tasks')
api.add_resource(ActualizarTarea, '/api/tasks/<int:id_task>')
api.add_resource(ObtenerTareas, '/api/tasks')
api.add_resource(ObtenerTarea, '/api/tasks/<int:id_task>')
api.add_resource(EliminarTarea, '/api/tasks/<int:id_task>')
api.add_resource(RecuperarArchivo, '/api/files/<filename>')
jwt = JWTManager(app)
