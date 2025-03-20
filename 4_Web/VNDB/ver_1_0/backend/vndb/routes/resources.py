import re
from abc import ABC, ABCMeta, abstractmethod
from flask import Blueprint, jsonify, abort, request
from vndb.tasks.resources import (
    get_resource_task, get_resources_task, 
    search_resource_task, search_resources_task,
    update_resource_task, update_resources_task, 
    delete_resource_task, delete_resources_task, 
    edit_resource_task, edit_resources_task,
)
from vndb.tasks.related_resources import (
    get_related_resources_task, search_related_resources_task,
    update_related_resources_task, delete_related_resources_task
)
from vndb.tasks.trash import (
    get_inactive_resource_task, get_inactive_resources_task,
    recover_resource_task, recover_resources_task,
    cleanup_resource_task, cleanup_resources_task
)
from .common import execute_task

class SingletonABCMeta(ABCMeta):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class BaseResourceBlueprint(ABC, metaclass=SingletonABCMeta):
    @abstractmethod
    def __init__(self, resource_type, plural_form=None, related_resources=None):
        self.resource_type = resource_type
        self.plural_form = plural_form or f'{resource_type}s'
        self.related_resources = related_resources or {}
        self.bp = Blueprint(self.plural_form, __name__)
        self.resource_bp = Blueprint(f'resource_{self.plural_form}', __name__, url_prefix=f'/{self.plural_form}')
        self.trash_bp = Blueprint(f'trash_{self.plural_form}', __name__, url_prefix=f'/trash/{self.plural_form}')

        self.register_routes()
        self.bp.register_blueprint(self.resource_bp)
        self.bp.register_blueprint(self.trash_bp)

    def register_routes(self):
        self.resource_bp.add_url_rule('', 'get_resources', self.get_resources, methods=['GET'])
        self.resource_bp.add_url_rule('/<string:id>', 'get_resource', self.get_resource, methods=['GET'])
        self.resource_bp.add_url_rule('', 'search_resources', self.search_resources, methods=['POST'])
        self.resource_bp.add_url_rule('/<string:id>', 'search_resource', self.search_resource, methods=['POST'])
        self.resource_bp.add_url_rule('', 'update_resources', self.update_resources, methods=['PUT'])
        self.resource_bp.add_url_rule('/<string:id>', 'update_resource', self.update_resource, methods=['PUT'])
        self.resource_bp.add_url_rule('', 'edit_resources', self.edit_resources, methods=['PATCH'])
        self.resource_bp.add_url_rule('/<string:id>', 'edit_resource', self.edit_resource, methods=['PATCH'])
        self.resource_bp.add_url_rule('', 'delete_resources', self.delete_resources, methods=['DELETE'])
        self.resource_bp.add_url_rule('/<string:id>', 'delete_resource', self.delete_resource, methods=['DELETE'])

        self.trash_bp.add_url_rule('', 'get_inactive_resources', self.get_inactive_resources, methods=['GET'])
        self.trash_bp.add_url_rule('/<string:id>', 'get_inactive_resource', self.get_inactive_resource, methods=['GET'])
        self.trash_bp.add_url_rule('', 'cleanup_resources', self.cleanup_resources, methods=['DELETE'])
        self.trash_bp.add_url_rule('/<string:id>', 'cleanup_resource', self.cleanup_resource, methods=['DELETE'])
        self.trash_bp.add_url_rule('', 'recover_resources', self.recover_resources, methods=['POST'])
        self.trash_bp.add_url_rule('/<string:id>', 'recover_resource', self.recover_resource, methods=['POST'])

        for endpoint, related_resource_type in self.related_resources.items():
            self.resource_bp.add_url_rule(f'/<string:id>/{endpoint}', f'get_related_{endpoint}', 
                                 lambda id, rt=related_resource_type: self.get_related_resources(id, rt), 
                                 methods=['GET'])
            self.resource_bp.add_url_rule(f'/<string:id>/{endpoint}', f'search_related_{endpoint}', 
                                 lambda id, rt=related_resource_type: self.search_related_resources(id, rt), 
                                 methods=['POST'])
            self.resource_bp.add_url_rule(f'/<string:id>/{endpoint}', f'update_related_{endpoint}', 
                                 lambda id, rt=related_resource_type: self.update_related_resources(id, rt), 
                                 methods=['PUT'])
            self.resource_bp.add_url_rule(f'/<string:id>/{endpoint}', f'delete_related_{endpoint}', 
                                 lambda id, rt=related_resource_type: self.delete_related_resources(id, rt), 
                                 methods=['DELETE'])

    def register_id_preprocessor(self):
        @self.resource_bp.url_value_preprocessor
        @self.trash_bp.url_value_preprocessor
        def check_id(endpoint, values):
            if 'id' in values:
                id_value = values['id']
                id_prefixes = {
                    'vn': 'v', 'character': 'c', 'staff': 's',
                    'tag': 't', 'producer': 'p', 'release': 'r', 'trait': 'i'
                }
                
                prefix = id_prefixes.get(self.resource_type)
                if prefix is None:
                    raise ValueError(f"Unknown resource type: {self.resource_type}")
                
                if not re.match(f'^{prefix}\d+$', id_value):
                    abort(400, description=f"Invalid id format for {self.resource_type}: {id_value}")

    def get_sync_param(self):
        return request.args.get('sync', 'true').lower() == 'true'

    def get_resources(self):
        args = request.args.to_dict()
        response_size = args.pop('response_size', 'small')
        page = args.pop('page', 1)
        limit = args.pop('limit', 20)
        sort = args.pop('sort', 'id')
        reverse = args.pop('reverse', False)
        count = args.pop('count', True)
        sync = self.get_sync_param()
        args.pop('sync', None)

        return execute_task(get_resources_task, sync, self.resource_type, args, response_size, page, limit, sort, reverse, count)

    def get_resource(self, id):
        args = request.args.to_dict()
        response_size = args.pop('response_size', 'small')
        sync = self.get_sync_param()
        args.pop('sync', None)
        return execute_task(get_resource_task, sync, self.resource_type, id, response_size)

    def search_resources(self):
        search_params = request.json
        response_size = search_params.pop('response_size', 'small')
        page = search_params.pop('page', 1)
        limit = search_params.pop('limit', 20)
        sort = search_params.pop('sort', 'id')
        reverse = search_params.pop('reverse', False)
        count = search_params.pop('count', True)
        sync = self.get_sync_param()

        return execute_task(search_resources_task, sync, self.resource_type, search_params, response_size, page, limit, sort, reverse, count)

    def search_resource(self, id):
        search_params = request.json
        response_size = search_params.pop('response_size', 'small')
        sync = self.get_sync_param()
        return execute_task(search_resource_task, sync, self.resource_type, id, response_size)

    def update_resources(self):
        sync = self.get_sync_param()
        return execute_task(update_resources_task, sync, self.resource_type)

    def update_resource(self, id):
        sync = self.get_sync_param()
        return execute_task(update_resource_task, sync, self.resource_type, id)

    def edit_resources(self):
        update_datas = request.json
        if not update_datas:
            return jsonify({"error": "No update data provided"}), 400
        
        if not isinstance(update_datas, list):
            return jsonify({"error": "Invalid format. Expected a list of updates"}), 400

        sync = self.get_sync_param()
        return execute_task(edit_resources_task, sync, self.resource_type, update_datas)

    def edit_resource(self, id):
        update_data = request.json
        if not update_data:
            return jsonify({"error": "No update data provided"}), 400
        
        sync = self.get_sync_param()
        return execute_task(edit_resource_task, sync, self.resource_type, id, update_data)

    def delete_resources(self):
        sync = self.get_sync_param()
        return execute_task(delete_resources_task, sync, self.resource_type)

    def delete_resource(self, id):
        sync = self.get_sync_param()
        return execute_task(delete_resource_task, sync, self.resource_type, id)

    def get_related_resources(self, id, related_resource_type):
        args = request.args
        response_size = args.get('response_size', 'small')
        page = args.get('page', default=1, type=int)
        limit = args.get('limit', default=20, type=int)
        sort = args.get('sort', default='id', type=str)
        reverse = args.get('reverse', default=False, type=bool)
        count = args.get('count', default=True, type=bool)
        sync = self.get_sync_param()
        return execute_task(get_related_resources_task, sync, self.resource_type, id, related_resource_type, response_size, page, limit, sort, reverse, count)

    def search_related_resources(self, id, related_resource_type):
        search_params = request.json
        response_size = search_params.pop('response_size', 'small')
        page = search_params.pop('page', 1)
        limit = search_params.pop('limit', 20)
        sort = search_params.pop('sort', 'id')
        reverse = search_params.pop('reverse', False)
        count = search_params.pop('count', True)
        sync = self.get_sync_param()
        return execute_task(search_related_resources_task, sync, self.resource_type, id, related_resource_type, response_size, page, limit, sort, reverse, count)

    def update_related_resources(self, id, related_resource_type):
        sync = self.get_sync_param()
        return execute_task(update_related_resources_task, sync, self.resource_type, id, related_resource_type)

    def delete_related_resources(self, id, related_resource_type):
        sync = self.get_sync_param()
        return execute_task(delete_related_resources_task, sync, self.resource_type, id, related_resource_type)

    def get_inactive_resources(self):
        args = request.args
        page = args.get('page', default=None, type=int)
        limit = args.get('limit', default=None, type=int)
        sort = args.get('sort', default='id', type=str)
        reverse = args.get('reverse', default=False, type=bool)
        count = args.get('count', default=True, type=bool)
        sync = self.get_sync_param()

        return execute_task(get_inactive_resources_task, sync, self.resource_type, page, limit, sort, reverse, count)

    def get_inactive_resource(self, id):
        sync = self.get_sync_param()
        return execute_task(get_inactive_resource_task, sync, self.resource_type, id)

    def cleanup_resources(self):
        sync = self.get_sync_param()
        return execute_task(cleanup_resources_task, sync, self.resource_type)

    def cleanup_resource(self, id):
        sync = self.get_sync_param()
        return execute_task(cleanup_resource_task, sync, self.resource_type, id)

    def recover_resources(self):
        sync = self.get_sync_param()
        return execute_task(recover_resources_task, sync, self.resource_type)

    def recover_resource(self, id):
        sync = self.get_sync_param()
        return execute_task(recover_resource_task, sync, self.resource_type, id)

    @property
    def blueprint(self):
        return self.bp

class VNResourceBlueprint(BaseResourceBlueprint):
    def __init__(self):
        related_resources = {
            "vns": "vn",
            "tags": "tag",
            "characters": "character",
            "producers": "producer",
            "staff": "staff",
            "releases": "release"
        }
        super().__init__('vn', related_resources=related_resources)

class CharacterResourceBlueprint(BaseResourceBlueprint):
    def __init__(self):
        related_resources = {
            "vns": "vn",
            "traits": "trait"
        }
        super().__init__('character', related_resources=related_resources)

class ReleaseResourceBlueprint(BaseResourceBlueprint):
    def __init__(self):
        related_resources = {
            "vns": "vn",
            "producers": "producer"
        }
        super().__init__('release', related_resources=related_resources)

class StaffResourceBlueprint(BaseResourceBlueprint):
    def __init__(self):
        related_resources = {
            "vns": "vn"
        }
        super().__init__('staff', plural_form='staff', related_resources=related_resources)

class TagResourceBlueprint(BaseResourceBlueprint):
    def __init__(self):
        related_resources = {
            "vns": "vn"
        }
        super().__init__('tag', related_resources=related_resources)

class TraitResourceBlueprint(BaseResourceBlueprint):
    def __init__(self):
        related_resources = {
            "characters": "character"
        }
        super().__init__('trait', related_resources=related_resources)

class ProducerResourceBlueprint(BaseResourceBlueprint):
    def __init__(self):
        related_resources = {
            "vns": "vn",
            "releases": "release"
        }
        super().__init__('producer', related_resources=related_resources)

vn_bp = VNResourceBlueprint().blueprint
character_bp = CharacterResourceBlueprint().blueprint
release_bp = ReleaseResourceBlueprint().blueprint
staff_bp = StaffResourceBlueprint().blueprint
tag_bp = TagResourceBlueprint().blueprint
trait_bp = TraitResourceBlueprint().blueprint
producer_bp = ProducerResourceBlueprint().blueprint