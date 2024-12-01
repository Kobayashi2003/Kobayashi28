from flask import jsonify, request, abort 

from api.tasks.related_resources import (
    get_related_resources_task,
    search_related_resources_task,
    update_related_resources_task,
    delete_related_resources_task
)
from .base import BaseResourceBlueprint

class CharacterResourceBlueprint(BaseResourceBlueprint):
    def __init__(self):
        super().__init__('character')
        self.register_additional_routes()

    def register_additional_routes(self):
        for endpoint, related_resource_type in {"vns":"vn", "traits":"trait"}.items():
            self.bp.add_url_rule('/<string:charid>/' + endpoint, 'get_related_' + endpoint, self.get_related_resources, methods=['GET'], defaults={"related_resource_type": related_resource_type})
            self.bp.add_url_rule('/<string:charid>/' + endpoint, 'search_related_' + endpoint, self.search_related_resources, methods=['POST'], defaults={"related_resource_type": related_resource_type})
            self.bp.add_url_rule('/<string:charid>/' + endpoint, 'update_related_' + endpoint, self.update_related_resources, methods=['PUT'], defaults={"related_resource_type": related_resource_type})
            self.bp.add_url_rule('/<string:charid>/' + endpoint, 'delete_related_' + endpoint, self.delete_related_resources, methods=['DELETE'], defaults={"related_resource_type": related_resource_type})

    def get_related_resources(self, charid, related_resource_type):
        args = request.args
        resopnse_size = args.get('response_size', 'small')
        page = args.get('page', default=1, type=int)
        limit = args.get('limit', default=20, type=int)
        sort = args.get('sort', default='id', type=str)
        reverse = args.get('reverse', default=False, type=bool)
        count = args.get('count', default=True, type=bool)

        return get_related_resources_task(
            'character', charid, related_resource_type, 
            resopnse_size, page, limit, sort, reverse, count)

    def search_related_resources(self, charid, related_resource_type):
        search_params = request.json
        response_size = search_params.pop('response_size', 'small')
        page = search_params.pop('page', 1)
        limit = search_params.pop('limit', 20)
        sort = search_params.pop('sort', 'id')
        reverse = search_params.pop('reverse', False)
        count = search_params.pop('count', True)

        return search_related_resources_task(
            "character", charid, related_resource_type, 
            response_size, page, limit, sort, reverse, count)

    def update_related_resources(self, charid, related_resource_type):
        task = update_related_resources_task.delay("character", charid, related_resource_type)
        return jsonify({"task_id": task.id}), 202

    def delete_related_resources(self, charid, related_resource_type):
        task = delete_related_resources_task.delay("character", charid, related_resource_type)
        return jsonify({"task_id": task.id}), 202

character_bp = CharacterResourceBlueprint().blueprint