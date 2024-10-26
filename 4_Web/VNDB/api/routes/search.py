from flask import Blueprint, request, jsonify, abort
from api.celery_app import celery
from api.tasks import search_task
from api.search.utils import VNDB_FIELDS_SIMPLE, LOCAL_FILELDS_SIMPLE

search_bp = Blueprint('search', __name__)

@search_bp.route('/api/search', methods=['GET'])
def search():
    search_type = request.args.get('searchType')
    
    if search_type == 'local':
        task = search_task.delay(
            search_type='local',
            filters={
                'id': request.args.get('localID'),
                'title': request.args.get('localTitle'),
                'developers': request.args.get('localDevelopers'),
                'characters': request.args.get('localCharacters'),
                'tags': request.args.get('localTags'),
                'length': request.args.get('localLength')
            },
            fields=LOCAL_FILELDS_SIMPLE
        )
    elif search_type == 'vndb':
        task = search_task.delay(
            search_type='vndb',
            filters = {
                'query': request.args.get('vndbQuery'),
                'developers': request.args.get('vndbDevelopers', '').split(','),
                'characters': request.args.get('vndbCharacters', '').split(','),
                'staffs': request.args.get('vndbStaffs', '').split(','),
                'released_date_expressions': request.args.get('vndbReleasedDate', '').split(','),
                'length': int(request.args.get('vndbLength')) if request.args.get('vndbLength') else None,
                'dev_status': int(request.args.get('vndbDevStatus')) if request.args.get('vndbDevStatus') else None,
                'has_description': request.args.get('vndbHasDescription') == 'on',
                'has_anime': request.args.get('vndbHasAnime') == 'on',
                'has_screenshot': request.args.get('vndbHasScreenshot') == 'on',
                'has_review': request.args.get('vndbHasReview') == 'on'
            },
            fields=VNDB_FIELDS_SIMPLE
        )
    else:
        abort(400, description="Invalid search type")
    
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