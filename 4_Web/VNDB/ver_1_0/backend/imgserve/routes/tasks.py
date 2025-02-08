from flask import Blueprint, jsonify 

from imgserve import celery

task_bp = Blueprint('tasks', __name__, url_prefix='/tasks')

def task_exists(tid):
    """Check if a task with the given ID exists."""
    return celery.backend.get(f'celery-task-meta-{tid}') is not None

@task_bp.route('/<string:tid>', methods=['GET'])
def get_task_result(tid: str):
    task = celery.AsyncResult(tid)
    if task.ready():
        return jsonify(task.result), 200
    return jsonify({'status': 'PENDING', 'results': task.state}), 202

@task_bp.route('/<string:tid>', methods=['POST'])
def revoke_task(tid: str):
    if not celery.backend.get(f'celery-task-meta-{tid}'):
        return jsonify({'status': 'NOT_FOUND', 'results': f'Task {tid} NOT_FOUND'}), 404
    try:
        task = celery.AsyncResult(tid)
        task.revoke(terminate=True)
        return jsonify({'status': 'SUCCESS'}), 200
    except Exception as e:
        return jsonify({'status': 'ERROR', 'results': str(e)}), 500