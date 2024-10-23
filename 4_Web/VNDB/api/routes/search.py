from flask import Blueprint, request, jsonify, abort

from api.search.local import search_local
from api.search.vndb import search_vndb
from api.search.helper import generate_fields, generate_filters

search_bp = Blueprint('search', __name__)

@search_bp.route('/api/search', methods=['GET'])
def search():
    search_type = request.args.get('searchType')
    
    if search_type == 'local':
        results = search_local(
            id=request.args.get('localID'),
            title=request.args.get('localTitle'),
            developers=request.args.get('localDevelopers'),
            characters=request.args.get('localCharacters'),
            tags=request.args.get('localTags'),
            length=request.args.get('localLength')
        )
    elif search_type == 'vndb':
        params = {
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
        }
        
        fields = generate_fields("id, title, released, image.thumbnail, image.sexual, image.violence")
        filters = generate_filters(**params)
        results = search_vndb(filters=filters, fields=fields)
        results = results['results'] if results else []
    else:
        abort(400, description="Invalid search type")
    
    return jsonify(results)

@search_bp.errorhandler(400)
def bad_request(e):
    return jsonify(error=str(e.description)), 400

@search_bp.errorhandler(404)
def not_found(e):
    return jsonify(error="Resource not found"), 404

@search_bp.errorhandler(500)
def server_error(e):
    return jsonify(error="An unexpected error occurred"), 500