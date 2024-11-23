from flask import jsonify, request, abort, send_file

from api.utils import get_image_path
from api.tasks.image import (
    get_images_task, upload_images_task, update_images_task, delete_images_task
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

    def get_character_images(self, charid):
        task = get_images_task.delay('character', charid)
        return jsonify({"task_id": task.id}), 202

    def get_character_image(self, charid, image_id):
        format = request.args.get('format', default='file', type=str)
        # TODO
        if format == 'file':
            image_path = get_image_path('character', charid, image_id)
            if not image_path:
                abort(400, 'Invalid image URL')
            return send_file(image_path, mimetype='image/jpeg')

        task = get_images_task.delay('character', charid, image_id)
        return jsonify({"task_id": task.id}), 202

    def upload_character_images(self, charid):
        if 'files' not in request.files:
            return jsonify({"error": "No file part"}), 400
        files = request.files.getlist('files')
        file_data = [{'filename': file.filename, 'content': file.read()} for file in files]

        task = upload_images_task.delay('character', charid, file_data)
        return jsonify({"task_id": task.id}), 202

    def update_character_images(self, charid):
        task = update_images_task.delay('character', charid)
        return jsonify({"task_id": task.id}), 202

    def update_character_image(self, charid, image_id):
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400
        file = request.files['file']
        file_data = {'filename': file.filename, 'content': file.read()}

        task = update_images_task.delay('character', charid, image_id, file_data)
        return jsonify({"task_id": task.id}), 202

    def delete_character_images(self, charid):
        task = delete_images_task.delay('character', charid)
        return jsonify({"task_id": task.id}), 202

    def delete_character_image(self, charid, image_id):
        task = delete_images_task.delay('character', charid, image_id)
        return jsonify({"task_id": task.id}), 202

character_bp = CharacterResourceBlueprint().blueprint

@character_bp.route('/<string:charid>/vns')
def cv1(charid: str): ...

@character_bp.route('/<string:charid>/vns/<string:vnid>')
def cv2(charid: str, vnid: str): ...

@character_bp.route('/<string:charid>/traits')
def ct1(charid: str): ...

@character_bp.route('/<string:charid>/traits/<string:trait_id>')
def ct2(charid: str, trait_id: str): ...