from datetime import datetime, timezone

from flask import Blueprint, jsonify

from api.tasks.backups import backup_task
from api.tasks.backups import restore_task
from api.tasks.backups import get_backups_task
from api.tasks.backups import delete_backups_task

backup_bp = Blueprint('backup', __name__, url_prefix='/backups')

@backup_bp.route('', methods=['GET'])
def get_backups():
    task = get_backups_task.delay()
    return jsonify({"task_id": task.id}), 202

@backup_bp.route('/<string:id>', methods=['GET'])
def get_backup(id):
    task = get_backups_task.delay(backup_id=id)
    return jsonify({"task_id": task.id}), 202

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
    task = delete_backups_task.delay(backup_id=id)
    return jsonify({"task_id": task.id}), 202