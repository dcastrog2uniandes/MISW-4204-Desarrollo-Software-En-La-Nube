from flask_jwt_extended import create_access_token

class Token:
    def crearToken(id):
        token = create_access_token(identity = id)
        return token