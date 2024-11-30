from flask import Blueprint, jsonify 

from api import celery

task_bp = Blueprint('tasks', __name__, url_prefix='/tasks')

def task_exists(task_id):
    """Check if a task with the given ID exists."""
    return celery.backend.get(f'celery-task-meta-{task_id}') is not None

@task_bp.route('', methods=['GET'])
def get_tasks_status():
    task_keys = celery.backend.client.keys('celery-task-meta-*')
    tasks_status = []
    for key in task_keys:
        task_id = key.decode().replace('celery-task-meta-', '')
        result = celery.AsyncResult(task_id)
        task_info = {
            'task_id': task_id,
            'status': result.status,
            'date_done': result.date_done.isoformat() if result.date_done else None,
        }
        tasks_status.append(task_info)

    return jsonify({
        'status': 'SUCCESS' if tasks_status else 'NOT_FOUND',
        'result': tasks_status,
    }), 200

@task_bp.route('/<string:task_id>', methods=['GET'])
def get_task_result(task_id: str):

    # if not task_exists(task_id):
    #     return jsonify(error=f'Task {task_id} not found'), 404

    task = celery.AsyncResult(task_id)

    if task.ready():
        return jsonify(task.result)

    return jsonify({
        'status': 'PENDING',
        'result': task.state
    }), 202

@task_bp.route('', methods=['POST'])
def revoke_tasks():
    revoke_results = {}

    task_keys = celery.backend.client.keys('celery-task-meta-*')
    for key in task_keys:
        task_id = key.decode().replace('celery-task-meta-', '')
        result = celery.AsyncResult(task_id)
        try:
            if result.state not in ['SUCCESS', 'FAILURE', 'REVOKED']:
                result.revoke(terminate=True)
            revoke_results[task_id] = True
        except Exception as e:
            revoke_results[task_id] = False

    return jsonify({
        'status': 'SUCCESS',
        'result': revoke_results
    }), 200

@task_bp.route('/<string:task_id>', methods=['POST'])
def revoke_task(task_id: str):

    if not task_exists(task_id):
        return jsonify(error=f'Task {task_id} not found'), 404

    try:
        task = celery.AsyncResult(task_id)
        task.revoke(terminate=True)
        return jsonify({'status': 'SUCCESS'}), 200
    except Exception as e:
        return jsonify({'status': 'ERROR', 'result': str(e)}), 500

@task_bp.route('', methods=['DELETE'])
def delete_all_tasks():
    delete_results = {}
    task_keys = celery.backend.client.keys('celery-task-meta-*')
    for key in task_keys:
        try:
            celery.backend.delete(key)
            delete_results[key] = True
        except:
            delete_results[key] = False

    return jsonify({
        'status': 'SUCCESS' if delete_results else 'NOT_FOUND',
        'result': delete_results
    }), 200

@task_bp.route('/<string:task_id>', methods=['DELETE'])
def delete_task(task_id: str):

    if not task_exists(task_id):
        return jsonify(error=f'Task {task_id} not found'), 404

    task = celery.AsyncResult(task_id)
    task.forget()
    return jsonify({'status': 'SUCCESS'}), 200

@task_bp.route('', methods=['PUT'])
def retry_tasks():
    return jsonify({'status': 'ERROR'})

@task_bp.route('/<string:task_id>', methods=['PUT'])
def retry_task(task_id: str):
    return jsonify({'status': 'ERROR'})
