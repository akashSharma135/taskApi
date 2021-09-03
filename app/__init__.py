from flask import Flask
import sys
from .db import start_db

db = start_db()

jwt = None

def create_app():
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = 'dd3ff1e5d693dda7482aa5f6e982da03'

    from flask_jwt_extended import JWTManager
    global jwt
    # Initializing JWTManager
    jwt = JWTManager(app)
    
    from app.api.manager import manager
    from app.api.admin import admin
    from app.api.user import user
    
    app.register_blueprint(manager, url_prefix='/')
    app.register_blueprint(user, url_prefix='/')
    app.register_blueprint(admin, url_prefix='/')
    
    return app