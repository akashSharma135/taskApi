from flask import Blueprint
from .auth import auth
from .task import task

user = Blueprint('user', __name__)

# user auth route blueprint registration
user.register_blueprint(auth, url_prefix='/auth')

user.register_blueprint(task, url_prefix='/task')
