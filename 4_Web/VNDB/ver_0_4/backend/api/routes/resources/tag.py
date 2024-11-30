from flask import request, jsonify

from .base import BaseResourceBlueprint
from api.tasks.related_resources import (
    get_related_resources_task,
    search_related_resources_task,
    update_related_resources_task,
    delete_related_resources_task
)

class TagResourceBlueprint(BaseResourceBlueprint):
    def __init__(self):
        super().__init__('tag')
        self.register_additional_routes()

    def register_additional_routes(self):
        self.bp.add_url_rule('/<string:id>/vns', 'get_related_vns', self.get_related_vns, methods=['GET'])
        self.bp.add_url_rule('/<string:id>/vns', 'search_related_vns', self.search_related_vns, methods=['POST'])
        self.bp.add_url_rule('/<string:id>/vns', 'update_related_vns', self.update_related_vns, methods=['PUT'])
        self.bp.add_url_rule('/<string:id>/vns', 'delete_related_vns', self.delete_related_vns, methods=['DELETE'])

    def get_related_vns(self, id):
        args = request.args
        response_size = args.get('response_size', 'small')
        page = args.get('page', default=1, type=int)
        limit = args.get('limit', default=20, type=int)
        sort = args.get('sort', default='id', type=str)
        reverse = args.get('reverse', default=False, type=bool)
        count = args.get('count', default=True, type=bool)
        return get_related_resources_task('tag', id, 'vn', response_size, page, limit, sort, reverse, count)

    def search_related_vns(self, id):
        search_params = request.json
        response_size = search_params.pop('response_size', 'small')
        page = search_params.pop('page', 1)
        limit = search_params.pop('limit', 20)
        sort = search_params.pop('sort', 'id')
        reverse = search_params.pop('reverse', False)
        count = search_params.pop('count', True)
        return search_related_resources_task('tag', id, 'vn', response_size, page, limit, sort, reverse, count)

    def update_related_vns(self, id):
        task = update_related_resources_task.delay('tag', id, 'vn')
        return jsonify({"task_id": task.id}), 202

    def delete_related_vns(self, id):
        task = delete_related_resources_task.delay('tag', id, 'vn')
        return jsonify({"task_id": task.id}), 202

tag_bp = TagResourceBlueprint().blueprint