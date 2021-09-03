from flask import Blueprint, abort
from flask.json import jsonify, request
from flask_jwt_extended import create_access_token
from app.api.utils import is_json_data, unique_id, hash_pwd, verify_pwd
from .token import access_token
from .. import db

auth = Blueprint('auth', __name__)

# manager signup auth route
@auth.route('/manager/signup', methods=['POST'])
def manager_signup():
    is_json_data()
    
    # Get the values from json
    manager_login = request.json.get("manager_login", None)
    name = request.json.get("name", None)
    password = request.json.get("password", None)
    
    # if any field is missing then abort with status 500
    if manager_login is None or password is None or name is None:
        abort(500)
        
    if db.managers.find_one({"manager_login": manager_login}):
        return jsonify(msg="manager_login already taken!")
    
    db.managers.insert_one({"id": unique_id(), "manager_login": manager_login, "name": name, "password": hash_pwd(password)})
    
    return jsonify(msg="account created")


# manager signin auth route
@auth.route('/manager/signin', methods=['POST'])
def manager_signin():
    if not request.json:
        return jsonify(msg="Missing JSON in request"), 500

    # Getting the values from json
    manager_login = request.json.get('manager_login', None)
    password = request.json.get('password', None)

    # Check if any of the field is empty, if yes then abort with status 500
    if not manager_login:
        return jsonify(msg="Missing manager_login parameter"), 500
    if not password:
        return jsonify(msg="Missing password parameter"), 500
    
    row = db.managers.find_one({"manager_login": manager_login})
    
    if not row:
        return jsonify(msg="wrong login id")
    
    
    # password verification
    if not verify_pwd(password, row.get('password')):
        return jsonify("password failed!"), 400
    
    # Generating the access token with identity = id
    return jsonify(access_token=access_token(row.get('id'))), 200




# user signup auth route
@auth.route('/user/signup', methods=['POST'])
def user_signup():
    is_json_data()
    
    # Get the values from json
    username = request.json.get("username", None)
    name = request.json.get("name", None)
    password = request.json.get("password", None)
    
    # if any field is missing then abort with status 500
    if username is None or password is None or name is None:
        abort(500)
        
    if db.users.find_one({"username": username}):
        return jsonify(msg="username already taken!")
    
    hashed_password = hash_pwd(password)
    
    db.users.insert_one({"id": unique_id(), "username": username, "name": name, "password": hashed_password, "manager_id": 'null'})
    
    return jsonify(msg="account created")


# user signin auth route
@auth.route('/user/signin', methods=['POST'])
def user_signin():
    is_json_data()

    # Getting the values from json
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    # Check if any of the field is empty, if yes then abort with status 500
    if not username:
        return jsonify(msg="Missing username parameter"), 500
    if not password:
        return jsonify(msg="Missing password parameter"), 500
    
    row = db.users.find_one({"username": username})
    
    if not row:
        return jsonify(msg="wrong login id")
    
    
    # password verification
    if not verify_pwd(password, row.get('password')):
        return jsonify("password failed!"), 400
    
    # Generating the access token with identity = id
    return jsonify(access_token=access_token(row.get('id'))), 200


# admin signin auth route
@auth.route('/admin/signin', methods=['POST'])
def admin_signin():
    is_json_data()

    login_id = request.json.get('login_id', None)
    password = request.json.get('password', None)

    if not login_id:
        return jsonify(message="Please! enter login_id")
    if not password:
        return jsonify(message="Please enter login password")

    if login_id != "admin":
        return jsonify({
            "msg": "login_id is incorrect"
        })

    if password != "admin":
        return jsonify({
            "msg": "password is incorrect"
        })

    return jsonify(access_token=access_token(login_id)), 200

