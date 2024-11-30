from flask import jsonify, request, abort 

from api.tasks.related_resources import (
    get_related_resources_task,
    search_related_resources_task,
    update_related_resources_task,
    delete_related_resources_task
)
from api.tasks.images import (
    get_image_task, get_images_task, 
    upload_image_task, upload_images_task, 
    update_image_task, update_images_task, 
    delete_image_task, delete_images_task
)
from .common import (
    get_image_file, create_images_zip
)
from .base import BaseResourceBlueprint

class CharacterResourceBlueprint(BaseResourceBlueprint):
    def __init__(self):
        super().__init__('character')
        self.register_additional_routes()

    def register_additional_routes(self):
        self.bp.add_url_rule('/<string:charid>/images', 'get_character_images', self.get_character_images, methods=['GET'])
        self.bp.add_url_rule('/<string:charid>/images/<string:image_id>', 'get_character_image', self.get_character_image, methods=['GET'])

        self.bp.add_url_rule('/<string:charid>/images', 'upload_character_images', self.upload_character_images, methods=['POST'])

        self.bp.add_url_rule('/<string:charid>/images', 'update_character_images', self.update_character_images, methods=['PUT'])
        self.bp.add_url_rule('/<string:charid>/images/<string:image_id>', 'update_character_image', self.update_character_image, methods=['PUT'])

        self.bp.add_url_rule('/<string:charid>/images', 'delete_character_images', self.delete_character_images, methods=['DELETE'])
        self.bp.add_url_rule('/<string:charid>/images/<string:image_id>', 'delete_character_image', self.delete_character_image, methods=['DELETE'])

        for endpoint, related_resource_type in {"vns":"vn", "traits":"trait"}.items():
            self.bp.add_url_rule('/<string:charid>/' + endpoint, 'get_related_' + endpoint, self.get_related_resources, methods=['GET'], defaults={"related_resource_type": related_resource_type})
            self.bp.add_url_rule('/<string:charid>/' + endpoint, 'search_related_' + endpoint, self.search_related_resources, methods=['POST'], defaults={"related_resource_type": related_resource_type})
            self.bp.add_url_rule('/<string:charid>/' + endpoint, 'update_related_' + endpoint, self.update_related_resources, methods=['PUT'], defaults={"related_resource_type": related_resource_type})
            self.bp.add_url_rule('/<string:charid>/' + endpoint, 'delete_related_' + endpoint, self.delete_related_resources, methods=['DELETE'], defaults={"related_resource_type": related_resource_type})

    def get_character_images(self, charid):
        format = request.args.get('format', default='json', type=str)
        if format =='file':
            return create_images_zip('character', charid)
        return get_images_task('character', charid)

    def get_character_image(self, charid, image_id):
        format = request.args.get('format', default='file', type=str)
        if format == 'file':
            return get_image_file('character', image_id)
        return get_image_task('character', charid, image_id)

    def upload_character_images(self, charid):
        if 'files' in request.files:
            files = request.files.getlist('files')
            files_data = [{'filename': file.filename, 'content': file.read()} for file in files]
            task = upload_images_task.delay('character', charid, files_data)
        elif 'file' in request.files:
            file = request.files['file']
            file_data = {'filename': file.filename, 'content': file.read()}
            task = upload_image_task.delay('character', charid, file_data)
        else:
            abort(400, 'No file part')
        return jsonify({"task_id": task.id}), 202

    def update_character_images(self, charid):
        task = update_images_task.delay('character', charid)
        return jsonify({"task_id": task.id}), 202

    def update_character_image(self, charid, image_id):
        task = update_image_task.delay('character', charid)
        return jsonify({"task_id": task.id}), 202

    def delete_character_images(self, charid):
        task = delete_images_task.delay('character', charid)
        return jsonify({"task_id": task.id}), 202

    def delete_character_image(self, charid, image_id):
        task = delete_image_task.delay('character', charid, image_id)
        return jsonify({"task_id": task.id}), 202

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