from flask import Blueprint, request, jsonify, abort

from api.celery_app import celery
from api.tasks import search_task

search_bp = Blueprint('search', __name__)

@search_bp.route('/api/search', methods=['GET', 'POST'])
def search():
    if request.method == 'GET':
        params = request.args
    elif request.method == 'POST':
        params = request.json
    else:
        abort(405)

    search_from = params.get('searchFrom', 'local')
    search_type = params.get('searchType', 'vn')
    response_size = params.get('responseSize', 'small')
    
    if search_from not in ['local', 'remote']:
        abort(400, description="Invalid search type")
    if search_type not in ['vn', 'character', 'tag', 'producer', 'staff', 'trait']:
        abort(400, description="Invalid search type")
    if response_size not in ['small', 'large']:
        abort(400, description="Invalid response size")
    
    task = search_task.delay(
        search_from=search_from,
        search_type=search_type,
        response_size=response_size,
        params=params
    )
    
    return jsonify({"task_id": task.id}), 202
    
@search_bp.route('/api/search/status/<task_id>', methods=['GET'])
def search_status(task_id):
    task = celery.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'status': 'Search is pending...'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'status': 'Search is in progress...'
        }
        if task.info:
            response['result'] = task.info
    else:
        response = {
            'state': task.state,
            'status': 'Search failed',
            'error': str(task.info)
        }
    return jsonify(response)
    
@search_bp.errorhandler(400)
def bad_request(e):
    return jsonify(error=str(e.description)), 400

@search_bp.errorhandler(404)
def not_found(e):
    return jsonify(error="Resource not found"), 404

@search_bp.errorhandler(500)
def server_error(e):
    return jsonify(error="An unexpected error occurred"), 500