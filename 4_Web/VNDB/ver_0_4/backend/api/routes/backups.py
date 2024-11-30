from flask import Blueprint, jsonify

from api.tasks.backups import (
    get_backup_task, get_backups_task, 
    delete_backup_task, delete_backups_task,
    backup_task, restore_task
)

backup_bp = Blueprint('backup', __name__, url_prefix='/backups')

@backup_bp.route('', methods=['GET'])
def get_backups():
    return get_backups_task()

@backup_bp.route('/<string:id>', methods=['GET'])
def get_backup(id):
    return get_backup_task(id)

@backup_bp.route('', methods=['POST'])
def backup():
    task = backup_task.delay()
    return jsonify({"task_id": task.id}), 202

@backup_bp.route('/<string:id>', methods=['POST'])
def restore(id):
    task = restore_task.delay(id)
    return jsonify({"task_id": task.id}), 202

@backup_bp.route('', methods=['DELETE'])
def delete_backups():
    task = delete_backups_task.delay()
    return jsonify({"task_id": task.id}), 202

@backup_bp.route('/<string:id>', methods=['DELETE'])
def delete_backup(id):
    task = delete_backup_task.delay(backup_id=id)
    return jsonify({"task_id": task.id}), 202