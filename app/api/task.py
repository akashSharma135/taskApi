from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.api.utils import is_json_data, unique_id
from .. import db

task = Blueprint('task', __name__)

# Assign task route
@task.route('/manager/assign-task', methods=['POST'])
@jwt_required()
def assign_task():
    is_json_data()
    
    # get the manager id of logged in manager
    current_manager_id = get_jwt_identity()
    
    if not db.managers.find_one({"id": current_manager_id}):
        return jsonify(msg='protected route')
    
    user_id = request.json.get('user_id')
    task_assigned = request.json.get('task_assigned')
    
    if not user_id:
        return jsonify(msg="Missing user_id parameter"), 500
    if not task_assigned:
        return jsonify(msg="Missing task_assigned parameter"), 500
    
    
    
    row = db.users.find_one({"id": user_id})
    if not row:
        return jsonify(msg="user doesn't exists")
    
    if row.get('manager_id') != current_manager_id:
        return jsonify(msg="You are not assigned to this user")
    
    row = db.tasks.find_one({"user_id": user_id})
    
    if row:
        return jsonify(msg="task is already assigned to the user")
    
    db.tasks.insert_one({"id": unique_id(), "task": task_assigned, "user_id": user_id, "manager_id": current_manager_id})
    
    return jsonify(msg="task assigned"), 200




# ====================================================================================================

# delete task route
@task.route('/delete-task', methods=['POST'])
@jwt_required()
def delete_task():
    is_json_data()
    
    # only admin
    if get_jwt_identity() != 'admin':
        return jsonify(msg="protected route")
    
    
    task_id = request.json.get('task_id')
    
    row = db.tasks.find_one({"id": task_id})
    
    if not row:
        return jsonify(msg="task does not exists")
    
    db.tasks.delete_one({"id": task_id})
    
    return jsonify(msg="task deleted")


# =========================================================================================================

# admin view task
@task.route('/admin/all-tasks')
@jwt_required()
def all_tasks():
    
    if get_jwt_identity() != 'admin':
        return jsonify(msg="protected route")
    
    task_list = []
    row = db.tasks.find({})
    
    for task in row:
        
        task_list.append({
            "task_id": task.get('id'),
            "task_assigned": task.get('task'),
            "task_assigned_to": db.users.find_one({"id": task.get('user_id')}).get('name'),
            "task_assigned_by": db.managers.find_one({"id": task.get('manager_id')}).get('name')
        })
        
        if len(task_list) < 1:
            return jsonify(msg="No tasks to show")
            
    
    return jsonify(task_list)
    

# Manager view task
@task.route('/task/manager/all-tasks')
@jwt_required()
def view_tasks():
    
    # only manager
    if not db.managers.find_one({"id": get_jwt_identity()}):
        return jsonify(msg='protected route')
    
    row = db.tasks.find({"manager_id": get_jwt_identity()})
    
    if not row:
        return jsonify(msg="You have not assigned any task")
    
    return jsonify(row)