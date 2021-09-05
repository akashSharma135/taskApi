from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required
from flask_jwt_extended.utils import get_jwt_identity
from app.api.utils import is_json_data
from .. import db
from .auth import auth
from .task import task

admin = Blueprint('admin', __name__)

# admin auth route blueprint registration
admin.register_blueprint(auth, url_prefix='/auth')

# 
admin.register_blueprint(task, url_prefix='/task')


# =========================================================================

# route for assigning manager to user
@admin.route('/admin/assign-manager', methods=['POST'])
@jwt_required()
def assign_task():
    is_json_data()
    
    if get_jwt_identity() != "admin":
        return jsonify(msg="protected route")

    # Getting the manager id and user id
    manager_id = request.json.get('manager_id')
    user_id = request.json.get('user_id')

    if not manager_id:
        return jsonify({"msg": "manager id not provided"}), 500
    if not user_id:
        return jsonify({"msg": "user id not provided"}), 500

    # check if manager exists
    if not db.managers.find_one({"id": manager_id}):
        return jsonify({
            "msg": f"No manager found with id: {manager_id}"
        })

    row = db.users.find_one({"id": user_id})

    # check if user exists
    if not row:
        return jsonify({
            "msg": f"No user found with id: {user_id}"
        })

    # check if manager is already assigned to the user
    if row.get('manager_id') != 'null':
        return jsonify({
            "msg": "manager is already assigned to this user"
        })

    db.users.update_one({"id": user_id}, {'$set': {"manager_id": manager_id}})

    return jsonify(msg="manager assigned"), 200


# =====================================================================================

# unassign manager
@admin.route('/admin/unassign-manager', methods=['POST'])
@jwt_required()
def unassign_task():
    is_json_data()
    
    # only admin
    if get_jwt_identity() != 'admin':
        return jsonify(msg="protected route")
    
    user_id = request.json.get('user_id')
    
    row = db.users.find_one({"id": user_id})
    
    if not row:
        return jsonify(msg="user does not exists")
    
    if row.get('manager_id') == 'null':
        return jsonify(msg="No manager to unassign")
    
    db.users.update_one({"id": user_id}, {'$set': {"manager_id": "null"}})
    
    db.tasks.delete_one({"user_id": user_id})
    
    return jsonify(msg="manager unassigned")