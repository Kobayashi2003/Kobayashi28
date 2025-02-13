from flask import Blueprint, abort, jsonify, request
from vndb.database import updatable
from vndb.tasks.resources import (
    update_resource_task, search_resources_task
)
from .common import execute_task

RESOURCE_TYPE_MAP = {
    'v': 'vn', 
    'r': 'release',
    'p': 'producer',
    'c': 'character',
    's': 'staff',
    'g': 'tag',
    'i': 'trait'
}

query_bp = Blueprint('query', __name__, url_prefix='/')

@query_bp.route('/<string:query>', methods=['GET'])
def handle_query(query):
    type = RESOURCE_TYPE_MAP.get(query[0].lower())
    if not type:
        abort(400, description="Invalid resource type")

    params = request.args.to_dict()

    if len(query) == 1:
        # Handle search for a specific type
        page = int(params.pop('page', 1))
        limit = int(params.pop('limit', 20))
        sort = params.pop('sort', 'id')
        reverse = params.pop('reverse', 'false').lower() == 'true'
        count = params.pop('count', 'true').lower() == 'true'

        search_from = params.pop('from', '')
        response_size = params.pop('size', 'large')

        if search_from in ['local', 'remote']:
            return execute_task(search_resources_task, 
                True, type, search_from, params, response_size, page, limit, sort, reverse, count)

        try:
            result = search_resources_task(
                type, 'remote', params, response_size, page, limit, sort, reverse, count)
            assert result['status'] == 'SUCCESS'
            return jsonify(result)
        except Exception as exc:
            return execute_task(search_resources_task, 
                True, type, 'local', params, response_size, page, limit, sort, reverse, count)

    elif len(query) > 1:
        # Handle get by ID
        try:
            int(query[1:])
        except ValueError:
            abort(400, description="Invalid ID format")

        search_from = params.pop('from', '')
        response_size = params.pop('size', 'large')


        if search_from == 'remote':
            if updatable(type, query):
                execute_task(update_resource_task, False, type, query)
            return execute_task(search_resources_task,
                True, type, 'remote', {'id':query}, response_size)
        elif search_from == 'local':
            return execute_task(search_resources_task,
                True, type, 'local', {'id':query}, response_size)

        try:
            assert updatable(type, query)
            execute_task(update_resource_task, False, type, query)
            result = search_resources_task(
                type, 'remote', {'id':query}, response_size, 1, 1, 'id', False, True)
            assert result['status'] == 'SUCCESS'
            return jsonify(result)
        except Exception as exc:
            return execute_task(search_resources_task,
                True, type, 'local', {'id':query}, response_size, 1, 1, 'id', False, True)

    else:
        abort(400, description="Invalid query")