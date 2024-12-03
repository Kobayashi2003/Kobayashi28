from flask import Blueprint, jsonify, request

from api.tasks.trash import (
    get_inactive_item_task, get_inactive_type_task,
    cleanup_item_task, cleanup_type_task,
    recover_item_task, recover_type_task 
)
from .common import execute_task

trash_bp = Blueprint('trash', __name__, url_prefix='/trash')

def get_sync_param():
    return request.args.get('sync', 'true').lower() == 'true'

@trash_bp.route('/<string:type>/<string:id>', methods=['GET'])
def get_item(type, id):
    sync = get_sync_param()
    return execute_task(get_inactive_item_task, sync, type, id)

@trash_bp.route('/<string:type>', methods=['GET'])
def get_type(type):
    args = request.args
    page = args.get('page', default=None, type=int)
    limit = args.get('limit', default=None, type=int)
    sort = args.get('sort', default='id', type=str)
    reverse = args.get('reverse', default=False, type=bool)
    count = args.get('count', default=True, type=bool)
    sync = get_sync_param()

    return execute_task(get_inactive_type_task, sync, type, page, limit, sort, reverse, count)

@trash_bp.route('/<string:type>/<string:id>', methods=['DELETE'])
def cleanup_item(type, id):
    sync = get_sync_param()
    return execute_task(cleanup_item_task, sync, type, id)

@trash_bp.route('/<string:type>', methods=['DELETE'])
def cleanup_type(type):
    sync = get_sync_param()
    return execute_task(cleanup_type_task, sync, type)

@trash_bp.route('/<string:type>/<string:id>', methods=['POST'])
def recover_item(type, id):
    sync = get_sync_param()
    return execute_task(recover_item_task, sync, type, id)

@trash_bp.route('/<string:type>', methods=['POST'])
def recover_type(type):
    sync = get_sync_param()
    return execute_task(recover_type_task, sync, type)