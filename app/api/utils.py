from flask import request, jsonify, abort
from passlib.hash import pbkdf2_sha256
import uuid
from .. import db

# check if the data is json
def is_json_data():
    if not request.json:
        return jsonify(msg="Not a json object"), 500
    
# hashes the password
def hash_pwd(password):
    return pbkdf2_sha256.hash(password)

# verifies the password
def verify_pwd(password, password_in_db):
    return pbkdf2_sha256.verify(password, password_in_db)

def unique_id():
    return str(uuid.uuid4())

