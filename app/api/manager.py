from .task import task
from flask import Blueprint
from .auth import auth

manager = Blueprint('manager', __name__)


# manager auth route blueprint registration
manager.register_blueprint(auth, url_prefix='/auth')

manager.register_blueprint(task, url_prefix='/task')


