from flask_jwt_extended import create_access_token

def access_token(identity):
    return create_access_token(identity=identity)