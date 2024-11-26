from datetime import datetime, timezone

from flask import jsonify, request, abort

from api import cache
from api.tasks.related_resources import (
    get_related_characters_images_task,
    update_related_characters_images_task, 
    delete_related_characters_images_task,
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
from api.tasks.savedatas import (
    get_savedata_task, get_savedatas_task, 
    upload_savedata_task, upload_savedatas_task, 
    delete_savedata_task, delete_savedatas_task,
)
from .common import (
    get_savedata_file, get_image_file,
    create_savedatas_zip, create_images_zip
)
from .base import BaseResourceBlueprint

class VNResourceBlueprint(BaseResourceBlueprint):
    def __init__(self):
        super().__init__('vn')
        self.register_additional_routes()

    def register_additional_routes(self):
        self.bp.add_url_rule('/<string:vnid>/images', 'get_vn_images', self.get_vn_images, methods=['GET'])
        self.bp.add_url_rule('/<string:vnid>/images/<string:image_id>', 'get_vn_image', self.get_vn_image, methods=['GET'])

        self.bp.add_url_rule('/<string:vnid>/images', 'upload_vn_images', self.upload_vn_images, methods=['POST'])

        self.bp.add_url_rule('/<string:vnid>/images', 'update_vn_images', self.update_vn_images, methods=['PUT'])
        self.bp.add_url_rule('/<string:vnid>/images/<string:image_id>', 'update_vn_image', self.update_vn_image, methods=['PUT'])

        self.bp.add_url_rule('/<string:vnid>/images', 'delete_vn_images', self.delete_vn_images, methods=['DELETE'])
        self.bp.add_url_rule('/<string:vnid>/images/<string:image_id>', 'delete_vn_image', self.delete_vn_image, methods=['DELETE'])


        self.bp.add_url_rule('/<string:vnid>/savedatas', 'get_vn_savedatas', self.get_vn_savedatas, methods=['GET'])
        self.bp.add_url_rule('/<string:vnid>/savedatas/<string:savedata_id>', 'get_vn_savedata', self.get_vn_savedata, methods=['GET'])

        self.bp.add_url_rule('/<string:vnid>/savedatas', 'upload_vn_savedatas', self.upload_vn_savedatas, methods=['POST'])

        self.bp.add_url_rule('/<string:vnid>/savedatas', 'delete_vn_savedatas', self.delete_vn_savedatas, methods=['DELETE'])
        self.bp.add_url_rule('/<string:vnid>/savedatas/<string:savedata_id>', 'delete_vn_savedata', self.delete_vn_savedata, methods=['DELETE'])


        for endpoint, related_resource_type in {"vns":"vn", "tags":"tag", "characters":"character", "producers":"producer", "staff":"staff"}.items():
            self.bp.add_url_rule('/<string:vnid>/' + endpoint, 'get_related_' + endpoint, self.get_related_resources, methods=['GET'], defaults={"related_resource_type": related_resource_type})
            self.bp.add_url_rule('/<string:vnid>/' + endpoint, 'search_related_' + endpoint, self.search_related_resources, methods=['POST'], defaults={"related_resource_type": related_resource_type})
            self.bp.add_url_rule('/<string:vnid>/' + endpoint, 'update_related_' + endpoint, self.update_related_resources, methods=['PUT'], defaults={"related_resource_type": related_resource_type})
            self.bp.add_url_rule('/<string:vnid>/' + endpoint, 'delete_related_' + endpoint, self.delete_related_resources, methods=['DELETE'], defaults={"related_resource_type": related_resource_type})

        self.bp.add_url_rule('/<string:vnid>/characters/images', 'get_related_characters_images', self.get_related_characters_images, methods=['GET'])
        self.bp.add_url_rule('/<string:vnid>/characters/images', 'update_related_characters_images', self.update_related_characters_images, methods=['PUT'])
        self.bp.add_url_rule('/<string:vnid>/characters/images', 'delete_related_characters_images', self.delete_related_characters_images, methods=['DELETE'])

    def get_vn_images(self, vnid):
        format = request.args.get('format', default='json', type=str)
        if format == 'file':
            return create_images_zip('vn', vnid)
        task = get_images_task.delay('vn', vnid)
        return jsonify({"task_id": task.id}), 202

    def get_vn_image(self, vnid, image_id):
        format = request.args.get('format', default='file', type=str)
        if format == 'file':
            return get_image_file('vn', image_id)
        task = get_image_task.delay('vn', vnid, image_id)
        return jsonify({"task_id": task.id}), 202

    def upload_vn_images(self, vnid):
        if 'files' in request.files:
            files = request.files.getlist('files')
            files_data = [{'filename': file.filename, 'content': file.read()} for file in files]
            task = upload_images_task.delay('vn', vnid, files_data)
        elif 'file' in request.files:
            file = request.files['file']
            file_data = {'filename': file.filename, 'content': file.read()}
            task = upload_image_task.delay('vn', vnid, file_data)
        else:
            abort(400, 'No file part')
        return jsonify({"task_id": task.id}), 202

    def update_vn_images(self, vnid):
        task = update_images_task.delay('vn', vnid)
        return jsonify({"task_id": task.id}), 202

    def update_vn_image(self, vnid, image_id):
        task = update_image_task.delay('vn', vnid, image_id)
        return jsonify({"task_id": task.id}), 202

    def delete_vn_images(self, vnid):
        task = delete_images_task.delay('vn', vnid)
        return jsonify({"task_id": task.id}), 202

    def delete_vn_image(self, vnid, image_id):
        task = delete_image_task.delay('vn', vnid, image_id)
        return jsonify({"task_id": task.id}), 202

    def get_vn_savedatas(self, vnid):
        format = request.args.get('format', default='json', type=str)
        if format == 'file':
            return create_savedatas_zip(vnid)
        task = get_savedatas_task.delay(vnid)
        return jsonify({"task_id": task.id}), 202

    def get_vn_savedata(self, vnid, savedata_id):
        format = request.args.get('format', default='file', type=str)
        if format == 'file':
            return get_savedata_file(savedata_id)
        task = get_savedata_task.delay(vnid, savedata_id)
        return jsonify({"task_id": task.id}), 202

    def upload_vn_savedatas(self, vnid):
        to_datetime = lambda ts: datetime.fromtimestamp(int(ts) / 1000.0, tz=timezone.utc) if ts else datetime.now(timezone.utc)
        if 'files' in request.files:
            files = request.files.getlist('files')
            files_data = [
                {
                    'filename': file.filename,
                    'content': file.read(),
                    'last_modified': to_datetime(request.form.get(f'last_modified_{file.filename}'))
                } for file in files
            ]
            task = upload_savedatas_task.delay(vnid, files_data)
        elif 'file' in request.files:
            file = request.files['file']
            file_data = {
                'filename': file.filename,
                'content': file.read(),
                'last_modified': to_datetime(request.form.get(f'last_modified_{file.filename}'))
            }
            task = upload_savedata_task.delay(vnid, file_data)
        else:
            abort(400, 'No file part')
        return jsonify({"task_id": task.id}), 202

    def delete_vn_savedatas(self, vnid):
        task = delete_savedatas_task.delay(vnid)
        return jsonify({"task_id": task.id}), 202

    def delete_vn_savedata(self, vnid, savedata_id):
        task = delete_savedata_task.delay(vnid, savedata_id)
        return jsonify({"task_id": task.id}), 202

    @cache.memoize(timeout=60)
    def get_related_characters_images(self, vnid):
        task = get_related_characters_images_task.delay(vnid)
        return jsonify({"task_id": task.id}), 202

    def update_related_characters_images(self, vnid):
        task = update_related_characters_images_task.delay(vnid)
        return jsonify({"task_id": task.id}), 202

    def delete_related_characters_images(self, vnid):
        task = delete_related_characters_images_task.delay(vnid)
        return jsonify({"task_id": task.id}), 202

    @cache.memoize(timeout=60)
    def get_related_resources(self, vnid, related_resource_type):
        task = get_related_resources_task.delay("vn", vnid, related_resource_type)
        return jsonify({"task_id": task.id}), 202

    @cache.memoize(timeout=60)
    def search_related_resources(self, vnid, related_resource_type):
        response_size = request.json.pop('response_size', 'small')
        task = search_related_resources_task.delay("vn", vnid, related_resource_type, response_size)
        return jsonify({"task_id": task.id}), 202

    def update_related_resources(self, vnid, related_resource_type):
        task = update_related_resources_task.delay("vn", vnid, related_resource_type)
        return jsonify({"task_id": task.id}), 202

    def delete_related_resources(self, vnid, related_resource_type):
        task = delete_related_resources_task.delay("vn", vnid, related_resource_type)
        return jsonify({"task_id": task.id}), 202

vn_bp = VNResourceBlueprint().blueprint