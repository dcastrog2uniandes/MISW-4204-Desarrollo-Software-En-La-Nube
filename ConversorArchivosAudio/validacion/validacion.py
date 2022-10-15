import numbers
import re
from flask_jwt_extended import create_access_token

class Validacion:
    def validacionParametroObligatorio(self, valor):
        if len(valor) == 0:
            return { "mensaje": "Parametro obligarotio", "codigo": 1003 }
        return ""

    def validacionParametros(self, request_json, parametro):
        try:
            request_json[parametro]
        except:
            return { "mensaje": "Parametro invalido", "codigo": 1004 }
        return ""
    
    def validacionNumeroEntero(self, valor):
        if not isinstance(valor, numbers.Integral):
            return { "mensaje": "El parametro no es numero entero", "codigo": 1005 }
        return ""

    def validacionFormatoEmail(self, valor):
        if not re.search('^[a-z0-9._%+-]+@[a-z0-9.-]+\\.[a-z]{2,4}$', valor):
            return { "mensaje": "El parametro no tiene formato de correo", "codigo": 1006}
        return ""