from flask import Blueprint
from .auth import auth

user = Blueprint('user', __name__)

# user auth route blueprint registration
user.register_blueprint(auth, url_prefix='/auth')
