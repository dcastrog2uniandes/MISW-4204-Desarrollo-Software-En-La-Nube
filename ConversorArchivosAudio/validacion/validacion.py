import numbers
import re
from modelos.modelos import db, Usuario
import os


class Validacion:
    def validacionParametros(self, response, request_json, parametro):
        try:
            request_json[parametro]
        except:
            response.errors += [{"error": { "mensaje": "Parametro {} no existe".format(parametro), "codigo": 1001 }}]

    def validacionParametroObligatorio(self, response,  request_json, parametro):
        if len(request_json[parametro]) == 0:
            response.errors += [{"error": { "mensaje": "Parametro {} obligarotio".format(parametro), "codigo": 1002 }}]

    
    def validacionNumeroEntero(self, response, request_json, parametro):
        try:
            int(request_json[parametro])
        except:
            response.errors += [{"error": { "mensaje": "El parametro {} no es numero entero".format(parametro), "codigo": 1003 }}]
         

    def validacionFormatoEmail(self, response, valor):
        if not re.search('^[a-z0-9._%+-]+@[a-z0-9.-]+\\.[a-z]{2,4}$', valor):
            response.errors += [{"error": { "mensaje": "El email no tiene formato valido", "codigo": 1004}}]
    
    def validacionCoincidenPasswords(self, response, password1, password2):
        if password1 != password2:
            response.errors += [{"error": { "mensaje": "Las contrasenas no coinciden", "codigo": 1005}}]

    def validacionUsernameExistente(self, response, username):
        if len(Usuario.query.filter(Usuario.username == username).all())>0:
            response.errors += [{"error": {"mensaje": "El usuario ya se encuentra registrado", "codigo": 1006}}]

    def validacionEmailExistente(self, response, email):
        if len(Usuario.query.filter(Usuario.email == email).all())>0:
            response.errors += [{"error": {"mensaje": "El email ya se encuentra registrado", "codigo": 1007}}]
    
    def validacionUsuarioNoEncontrado(self, response, username):
        if len(Usuario.query.filter(Usuario.username == username).all()) == 0:
            response.errors += [{"error": {"mensaje": "El usuario no se encuentra registrado", "codigo": 404}}]
    
    def validacionContrasenaUsuario(self, response, username, password):
        if Usuario.query.filter(Usuario.username == username).all()[0].password != password:
            response.errors += [{"error": {"mensaje": "Contrasena no valida", "codigo": 404}}]

    def validacionExisteArchivo(self, response, filepath):
        file_exists = os.path.exists(filepath)
        if not file_exists:
            response.errors += [{"error": {"mensaje": "El archivo no existe", "codigo": 1008}}]            

    def validacionFormatoArchivo(self, response, filepath):
        formats = ['.wav','.ogg','.mp3']
        root, extension = os.path.splitext(filepath)
        if extension not in formats:
            response.errors += [{"error": {"mensaje": "El formato no es valido", "codigo": 1009}}]

    def validacionTamanioMax(self, response, filepath):
        file_size = os.path.getsize(filepath) 
        print(file_size)
        if file_size > 5000000:
            response.errors += [{"error": {"mensaje": "El archivo excede el tamaño maximo", "codigo": 1010}}]


        
