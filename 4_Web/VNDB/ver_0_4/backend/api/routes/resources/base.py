from flask import Blueprint, jsonify, request
from abc import ABC, ABCMeta, abstractmethod

from api.tasks.resources import (
    get_resource_task, get_resources_task, 
    search_resource_task, search_resources_task,
    update_resource_task, update_resources_task, 
    delete_resource_task, delete_resources_task, 
    edit_resource_task, edit_resources_task
)

class SingletonABCMeta(ABCMeta):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class BaseResourceBlueprint(ABC, metaclass=SingletonABCMeta):
    @abstractmethod
    def __init__(self, resource_type, plural_form=None):
        self.resource_type = resource_type
        self.plural_form = plural_form or f'{resource_type}s'
        self.bp = Blueprint(self.plural_form, __name__, url_prefix=f'/{self.plural_form}')
        self.register_routes()

    def register_routes(self):
        self.bp.add_url_rule('', 'get_resources', self.get_resources, methods=['GET'])
        self.bp.add_url_rule('/<string:id>', 'get_resource', self.get_resource, methods=['GET'])
        self.bp.add_url_rule('', 'search_resources', self.search_resources, methods=['POST'])
        self.bp.add_url_rule('/<string:id>', 'search_resource_by_id', self.search_resource_by_id, methods=['POST'])
        self.bp.add_url_rule('', 'update_resources', self.update_resources, methods=['PUT'])
        self.bp.add_url_rule('/<string:id>', 'update_resource', self.update_resource, methods=['PUT'])
        self.bp.add_url_rule('', 'edit_resources', self.edit_resources, methods=['PATCH'])
        self.bp.add_url_rule('/<string:id>', 'edit_resource', self.edit_resource, methods=['PATCH'])
        self.bp.add_url_rule('', 'delete_resources', self.delete_resources, methods=['DELETE'])
        self.bp.add_url_rule('/<string:id>', 'delete_resource', self.delete_resource, methods=['DELETE'])

    def get_resources(self):
        args = request.args
        page = args.get('page', default=None, type=int)
        limit = args.get('limit', default=None, type=int)
        sort = args.get('sort', default='id', type=str)
        reverse = args.get('reverse', default=False, type=bool)
        count = args.get('count', default=True, type=bool)

        return get_resources_task(self.resource_type, page, limit, sort, reverse)

    def get_resource(self, id):
        return get_resource_task(self.resource_type, id)

    def search_resources(self):
        search_params = request.json
        search_from = search_params.pop('search_from', 'local')
        response_size = search_params.pop('response_size', 'small')
        page = search_params.pop('page', 1)
        limit = search_params.pop('limit', 20)
        sort = search_params.pop('sort', 'id')
        reverse = search_params.pop('reverse', False)
        count = search_params.pop('count', True)

        return search_resources_task(self.resource_type, search_from, search_params, response_size, page, limit, sort, reverse, count)

    def search_resource_by_id(self, id):
        return search_resource_task(self.resource_type, id)

    def update_resources(self):
        task = update_resources_task.delay(self.resource_type)
        return jsonify({"task_id": task.id}), 202

    def update_resource(self, id):
        task = update_resource_task.delay(self.resource_type, id)
        return jsonify({"task_id": task.id}), 202

    def edit_resources(self):
        update_datas = request.json
        if not update_datas:
            return jsonify({"error": "No update data provided"}), 400
        
        if not isinstance(update_datas, list):
            return jsonify({"error": "Invalid format. Expected a list of updates"}), 400

        task = edit_resources_task.delay(self.resource_type, update_datas)
        return jsonify({"task_id": task.id}), 202

    def edit_resource(self, id):
        update_data = request.json
        if not update_data:
            return jsonify({"error": "No update data provided"}), 400
        
        task = edit_resource_task.delay(self.resource_type, id, update_data)
        return jsonify({"task_id": task.id}), 202

    def delete_resources(self):
        task = delete_resources_task.delay(self.resource_type)
        return jsonify({"task_id": task.id}), 202

    def delete_resource(self, id):
        task = delete_resource_task.delay(self.resource_type, id)
        return jsonify({"task_id": task.id}), 202

    @property
    def blueprint(self):
        return self.bp