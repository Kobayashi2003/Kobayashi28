from flask import Blueprint, abort, jsonify, request
from vndb.tasks.resources import (
    search_resources_task, search_remote_and_update_database_task
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
    ignore_small_response = False

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

        if search_from == 'local':
            return execute_task(search_resources_task, 
                True, type, 'local', params, response_size, page, limit, sort, reverse, count)
        elif search_from == 'remote':
            return execute_task(search_remote_and_update_database_task,
                True, type, params, response_size, page, limit, sort, reverse, count, ignore_small_response=ignore_small_response)

        try:
            func_return = search_remote_and_update_database_task(
                type, params, response_size, page, limit, sort, reverse, count, ignore_small_response=ignore_small_response)
            assert func_return['status'] == 'SUCCESS'
            return jsonify(func_return)
        except Exception as exc:
            print(f"Error in search_remote_and_update_database_task: {exc}")
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
            return execute_task(search_remote_and_update_database_task,
                True, type, {'id':query}, response_size, 1, 1, 'id', False, True, ignore_small_response=ignore_small_response)
        elif search_from == 'local':
            return execute_task(search_resources_task,
                True, type, 'local', {'id':query}, response_size, 1, 1, 'id', False, True)

        try:
            func_return = search_remote_and_update_database_task(
                type, {'id':query}, response_size, 1, 1, 'id', False, True, ignore_small_response=ignore_small_response)
            assert func_return['status'] == 'SUCCESS'
            return jsonify(func_return)
        except Exception as exc:
            print(f"Error in search_remote_and_update_database_task: {exc}")
            return execute_task(search_resources_task,
                True, type, 'local', {'id':query}, response_size, 1, 1, 'id', False, True)

    else:
        abort(400, description="Invalid query")