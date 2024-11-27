from flask import Blueprint, jsonify 

from api.tasks.trash import (
    _get_inactive_item_task, _get_inactive_type_task, _get_inactive_all_task,
    cleanup_item_task, cleanup_type_task, cleanup_all_task,
    recover_item_task, recover_type_task, recover_all_task
)

def get_inactive_item_task(*args, **kwargs): return _get_inactive_item_task(*args, **kwargs)

def get_inactive_type_task(*args, **kwargs): return _get_inactive_type_task(*args, **kwargs)

def get_inactive_all_task(*args, **kwargs): return _get_inactive_all_task(*args, **kwargs)

trash_bp = Blueprint('trash', __name__, url_prefix='/trash')

@trash_bp.route('/<string:type>/<string:id>', methods=['GET'])
def get_item(type, id):
    return get_inactive_item_task(type, id)

@trash_bp.route('/<string:type>', methods=['GET'])
def get_type(type):
    return get_inactive_type_task(type)

@trash_bp.route('', methods=['GET'])
def get_all():
    return get_inactive_all_task()

@trash_bp.route('/<string:type>/<string:id>', methods=['DELETE'])
def cleanup_item(type, id):
    task = cleanup_item_task.delay(type, id)
    return jsonify({"task_id": task.id}), 202

@trash_bp.route('/<string:type>', methods=['DELETE'])
def cleanup_type(type):
    task = cleanup_type_task.delay(type)
    return jsonify({"task_id": task.id}), 202

@trash_bp.route('', methods=['DELETE'])
def cleanup_all():
    task = cleanup_all_task.delay()
    return jsonify({"task_id": task.id}), 202

@trash_bp.route('/<string:type>/<string:id>', methods=['POST'])
def recover_item(type, id):
    task = recover_item_task.delay(type, id)
    return jsonify({"task_id": task.id}), 202

@trash_bp.route('/<string:type>', methods=['POST'])
def recover_type(type):
    task = recover_type_task.delay(type)
    return jsonify({"task_id": task.id}), 202

@trash_bp.route('', methods=['POST'])
def recover_all():
    task = recover_all_task.delay()
    return jsonify({"task_id": task.id}), 202