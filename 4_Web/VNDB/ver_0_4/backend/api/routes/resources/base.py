from flask import Blueprint, jsonify, request
from abc import ABC, ABCMeta, abstractmethod
from api.tasks.resource import (
    get_resources_task, search_resource_task, search_resources_task,
    update_resources_task, delete_resources_task, edit_resources_task
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
        page = request.args.get('page', default=1, type=int)
        limit = request.args.get('limit', default=20, type=int)
        sort = request.args.get('sort', default='id', type=str)
        order = request.args.get('order', default='asc', type=str)
        
        task = get_resources_task.delay(self.resource_type, None, page, limit, sort, order)
        return jsonify({"task_id": task.id}), 202

    def get_resource(self, id):
        task = get_resources_task.delay(self.resource_type, id)
        return jsonify({"task_id": task.id}), 202

    def search_resources(self):
        search_params = request.json
        search_from = search_params.pop('search_from', 'local')
        response_size = search_params.pop('response_size', 'small')
        page = search_params.pop('page', 1)
        limit = search_params.pop('limit', 20)
        sort = search_params.pop('sort', 'id')
        order = search_params.pop('order', 'asc')
        
        task = search_resources_task.delay(self.resource_type, search_from, search_params, response_size, page, limit, sort, order)
        return jsonify({"task_id": task.id}), 202

    def search_resource_by_id(self, id):
        task = search_resource_task.delay(self.resource_type, id)
        return jsonify({"task_id": task.id}), 202

    def update_resources(self):
        task = update_resources_task.delay(self.resource_type)
        return jsonify({"task_id": task.id}), 202

    def update_resource(self, id):
        task = update_resources_task.delay(self.resource_type, id)
        return jsonify({"task_id": task.id}), 202

    def edit_resources(self):
        updates = request.json
        if not updates:
            return jsonify({"error": "No update data provided"}), 400
        
        if not isinstance(updates, list):
            return jsonify({"error": "Invalid format. Expected a list of updates"}), 400

        task = edit_resources_task.delay(self.resource_type, updates)
        return jsonify({"task_id": task.id}), 202

    def edit_resource(self, id):
        update_data = request.json
        if not update_data:
            return jsonify({"error": "No update data provided"}), 400
        
        update_data['id'] = id  # Ensure the id is included in the update data
        task = edit_resources_task.delay(self.resource_type, update_data)
        return jsonify({"task_id": task.id}), 202

    def delete_resources(self):
        task = delete_resources_task.delay(self.resource_type)
        return jsonify({"task_id": task.id}), 202

    def delete_resource(self, id):
        task = delete_resources_task.delay(self.resource_type, id)
        return jsonify({"task_id": task.id}), 202

    @property
    def blueprint(self):
        return self.bp