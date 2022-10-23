import numbers
import re
from modelos.modelos import db, Usuario, Tarea
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

    def validacionFormatoActualizado(self, response, formato_request):
        formats = ['.wav','.ogg','.mp3']
        if formato_request not in formats:
            response.errors += [{"error": {"mensaje": "El formato no es valido", "codigo": 1009}}]

    def validacionTamanioMax(self, response, filepath):
        file_size = os.path.getsize(filepath) 
        if file_size < 5000000:
            response.errors += [{"error": {"mensaje": "El archivo debe ser mayor o igual el tamanio", "codigo": 1010}}]

    def validacionTareaExistente(self, response, id_task):
        if len(Tarea.query.filter(Tarea.id == id_task).all()) == 0:
            response.errors += [{"error": {"mensaje": "La tarea con el id {}, no existe".format(id_task), "codigo": 404}}]

    def validacionIdUsuarioNoEncontrado(self, response, id):
        if len(Usuario.query.filter(Usuario.id == id).all()) == 0:
            response.errors += [{"error": {"mensaje": "El usuario con ese id no se encuentra registrado", "codigo": 404}}]

    def validacionParametroOpcionalExistente(self, headers, parametro):
        try:
            headers[parametro]
            return True
        except:
            return False

    def validacionListaDeValores(self, response, request_json, parametro, lista):
        if len([i for i in lista if i == request_json[parametro]]) == 0:
            response.errors += [{"error": { "mensaje": "El parametro {} no tiene valor valido".format(parametro), "codigo": 1011 }}]

    def validacionArchivoNoEncontrado(self, response, id, filename):
        totalArchivos =  [ta.fileOriginal for ta in Tarea.query.filter(Tarea.usuario == id).all() if ta.fileOriginal is not None] + [ta.fileConvertido for ta in Tarea.query.filter(Tarea.usuario == id).all() if ta.fileConvertido is not None]
        if (len(totalArchivos) == 0):
            response.errors += [{"error": {"mensaje": "El usuario no tiene archivos".format(filename), "codigo": 404}}]
        elif len([a for a in totalArchivos if a.split('/')[-1] == filename] ) == 0:
            response.errors += [{"error": {"mensaje": "El archivo {} no fue encontrado".format(filename), "codigo": 404}}]

    def validacionExisteArchivoDestino(self, response, filepath):
        root, file_name = os.path.split(filepath)
        file_exists = os.path.exists('../Archivos/ArchivoOriginal/'+file_name)
        if file_exists:
            response.errors += [{"error": {"mensaje": "Existe un archivo con este nombre en el destinio", "codigo": 1012}}]

    def validacionExisteArchivoActualizar(self, filepath):
        return os.path.exists(filepath)
        
    def validacionFormatoArchivoDestino(self, response, filepath, newFormat):
        root, extension = os.path.splitext(filepath)
        if extension == newFormat:
            response.errors += [{"error": {"mensaje": "La extension origen es igual a la extension destino", "codigo": 1013}}]

    def validacionArchivoNoEstaDescargado(self,response, filepath, filename):
        if os.path.exists(filepath + '/' + filename):
            response.errors += [{"error": {"mensaje": "Ya se encuentra un archivo con el nombre {} en la ruta {}".format(filename, filepath)}, "codigo": 1014}]

    def validacionUsuarioSinTareas(self, response, id_usuario):
        if len(Tarea.query.filter(Tarea.usuario == id_usuario).all()) == 0:
            response.errors += [{"error": {"mensaje": "El usuario no tiene tareas", "codigo": 1015}}]