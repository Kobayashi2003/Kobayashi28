from flask import abort, request
from vndb.database import updatable
from vndb.tasks.resources import (
    get_resource_task, update_resource_task, 
    search_resource_task, search_resources_task
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

def handle_query(query):
    type = RESOURCE_TYPE_MAP.get(query[0].lower())
    if not type:
        abort(400, description="Invalid resource type")

    if len(query) == 1:
        # Handle search for a specific type
        params = request.args.to_dict()
        page = int(params.pop('page', 1))
        limit = int(params.pop('limit', 20))
        sort = params.pop('sort', 'id')
        reverse = params.pop('reverse', 'false').lower() == 'true'
        count = params.pop('count', 'true').lower() == 'true'
        try:
            return execute_task(search_resources_task, 
                True, type, 'remote', params, 'large', page, limit, sort, reverse, count)
        except:
            return execute_task(search_resources_task, 
                True, type, 'local', params, 'large', page, limit, sort, reverse, count)

    elif len(query) > 1:
        # Handle get by ID
        try:
            int(query[1:])
        except ValueError:
            abort(400, description="Invalid ID format")

        if updatable(type, query):
            try:
                execute_task(update_resource_task, False, type, query)
                return execute_task(search_resource_task, True, type, query, 'large')
            except:
                return execute_task(get_resource_task, True, type, query)
        else:
            return execute_task(get_resource_task, True, type, query)

    else:
        abort(400, description="Invalid query")