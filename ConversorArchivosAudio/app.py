from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api
from registro.registro import Registro
from crearTarea.creartarea import CrearTarea
from obtenerTareas.obtenerTareas import ObtenerTareas
from obtenerTarea.obtenerTarea import ObtenerTarea 
from eliminarTarea.eliminarTarea import EliminarTarea
from login.login import Login
from actualizarTarea.actualizatarea import ActualizarTarea
from recuperarArchivo.recuperarArchivo import RecuperarArchivo
from conectarBD.conectarBD import ConectarBD

app = Flask(__name__)
conectar = ConectarBD()
conectar.conectar(app)

app.config['JWT_SECRET_KEY'] = 'frase-secreta'
app.config['PROPAGATE_EXCEPTIONS'] = True

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
