import numbers
class Validacion:
    def validacionParametroObligatorio(valor):
        if len(valor) == 0:
            return { "mensaje": "Parametro obligarotio", "codigo": 1003 }

    def validacionParametros(request_json, parametro):
        try:
            request_json[parametro]
        except:
            return { "mensaje": "Parametro invalido", "codigo": 1004 }
    
    def validacionNumeroEntero(valor):
        if not isinstance(valor, numbers.Integral):
            return { "mensaje": "El parametro no es numero entero", "codigo": 1005 }
    
    