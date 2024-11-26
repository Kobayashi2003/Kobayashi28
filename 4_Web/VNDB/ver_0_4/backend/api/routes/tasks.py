from flask import Blueprint, jsonify 
from celery.states import PENDING, SUCCESS, FAILURE, STARTED, RETRY 
from celery.backends.base import BaseBackend
from celery.exceptions import TaskRevokedError

from api import celery, cache

task_bp = Blueprint('tasks', __name__, url_prefix='/tasks')

def task_exists(task_id):
    """Check if a task with the given ID exists."""
    return celery.backend.get(f'celery-task-meta-{task_id}') is not None

@task_bp.route('', methods=['GET'])
def get_all_tasks_status():
    try:
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
            'tasks': tasks_status,
            'total_tasks': len(tasks_status)
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'Failed to retrieve task statuses',
            'message': str(e)
        }), 500

@task_bp.route('/<string:task_id>', methods=['GET'])
def get_task_status(task_id: str):

    if not task_exists(task_id):
        return jsonify({'message': f'Task {task_id} not found'}), 404

    task = celery.AsyncResult(task_id)
    
    if task.state == PENDING:
        response = {
            'state': task.state,
            'status': 'Task is waiting for execution'
        }
    elif task.state == STARTED:
        response = {
            'state': task.state,
            'status': 'Task has been started'
        }
    elif task.state == SUCCESS:
        response = {
            'state': task.state,
            'status': 'Task has been completed successfully',
        }
    elif task.state == FAILURE:
        response = {
            'state': task.state,
            'status': 'Task execution failed',
            'error': str(task.info)
        }
    elif task.state == RETRY:
        response = {
            'state': task.state,
            'status': 'Task is being retried'
        }
    else:
        response = {
            'state': task.state,
            'status': 'Unknown task state'
        }
    
    return jsonify(response)

@task_bp.route('/<string:task_id>/result', methods=['GET'])
@cache.memoize(timeout=60)
def get_task_result(task_id: str):

    if not task_exists(task_id):
        return jsonify({'message': f'Task {task_id} not found'}), 404

    task = celery.AsyncResult(task_id)

    if task.ready():
        return jsonify(task.result)

    return jsonify({'state': task.state}), 202

@task_bp.route('', methods=['POST'])
def revoke_all_tasks():
    try:
        task_keys = celery.backend.client.keys('celery-task-meta-*')
        revoked_count = 0
        for key in task_keys:
            task_id = key.decode().replace('celery-task-meta-', '')
            result = celery.AsyncResult(task_id)
            if result.state not in ['SUCCESS', 'FAILURE', 'REVOKED']:
                result.revoke(terminate=True)
                revoked_count += 1

        return jsonify({
            'message': f'Revoked {revoked_count} tasks',
            'revoked_count': revoked_count,
            'total_tasks': len(task_keys)
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'Failed to revoke tasks',
            'message': str(e)
        }), 500

@task_bp.route('/<string:task_id>', methods=['POST'])
def revoke_task(task_id: str):
    if not task_exists(task_id):
        return jsonify({'message': f'Task {task_id} not found'}), 404
    try:
        task = celery.AsyncResult(task_id)
        # Attempt to revoke (cancel) the task
        task.revoke(terminate=True)
        return jsonify({'message': f'Task {task_id} has been cancelled'}), 200
    except TaskRevokedError:
        # Task was already revoked
        return jsonify({'message': f'Task {task_id} was already cancelled'}), 200
    except Exception as e:
        # Any other error
        return jsonify({'error': f'Failed to cancel task {task_id}', 'message': str(e)}), 500

@task_bp.route('', methods=['DELETE'])
def delete_all_tasks():
    try:
        task_keys = celery.backend.client.keys('celery-task-meta-*')
        deleted_count = 0
        for key in task_keys:
            celery.backend.delete(key)
            deleted_count += 1

        return jsonify({
            'message': f'Deleted {deleted_count} task results',
            'deleted_count': deleted_count,
            'total_tasks': len(task_keys)
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'Failed to delete task results',
            'message': str(e)
        }), 500

@task_bp.route('/<string:task_id>', methods=['DELETE'])
def delete_task(task_id: str):
    if not task_exists(task_id):
        return jsonify({'message': f'Task {task_id} not found'}), 404
    try:
        task = celery.AsyncResult(task_id)
        # Attempt to forget (delete) the task result
        task.forget()
        return jsonify({'message': f'Task {task_id} has been deleted'}), 200
    except BaseBackend.TaskNotFound:
        # Task result was not found
        return jsonify({'message': f'Task {task_id} not found'}), 404
    except Exception as e:
        # Any other error
        return jsonify({'error': f'Failed to delete task {task_id}', 'message': str(e)}), 500

@task_bp.route('', methods=['PUT'])
def retry_tasks():
    ... # TODO

@task_bp.route('/<string:task_id>', methods=['PUT'])
def retry_task(task_id: str):
    ... # TODO
