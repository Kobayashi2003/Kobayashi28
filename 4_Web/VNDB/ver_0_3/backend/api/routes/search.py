from flask import Blueprint, request, jsonify, abort
from api.celery_app import celery
from api.tasks import search_task
from api.search.utils import VNDB_FIELDS_SMALL, LOCAL_FIELDS_SMALL
from api.search.utils import VNDB_FIELDS_LARGE, LOCAL_FIELDS_LARGE
from api.routes.utils import get_filters

search_bp = Blueprint('search', __name__)

@search_bp.route('/api/search', methods=['GET'])
def search():
    search_type = request.args.get('searchType')
    
    if search_type not in ['local', 'vndb']:
        abort(400, description="Invalid search type")
    
    filters = get_filters(search_type)
    responseSize = request.args.get('responseSize', 'small')
    if responseSize == 'small':
        fields = (LOCAL_FIELDS_SMALL if search_type == 'local' else VNDB_FIELDS_SMALL)
    elif responseSize == 'large':
        fields = (LOCAL_FIELDS_LARGE if search_type == 'local' else VNDB_FIELDS_LARGE)
    else:
        abort(400, description="Invalid response size")
    
    task = search_task.delay(
        search_type=search_type,
        filters=filters,
        fields=fields
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