from .base import BaseResourceBlueprint
from flask import jsonify, request, abort, send_file
from io import BytesIO
import zipfile
from datetime import datetime, timezone
from api.database import get_image_path, get_savedata_path, get_savedatas, get
from api.tasks.image import (
    get_images_task, upload_images_task, update_images_task, delete_images_task
)
from api.tasks.savedata import (
    get_savedatas_task, upload_savedatas_task, delete_savedatas_task
)
from api.tasks.resource import delete_vns_task

class VNResourceBlueprint(BaseResourceBlueprint):
    def __init__(self):
        super().__init__('vn')
        self.register_additional_routes()

    def register_additional_routes(self):
        self.bp.add_url_rule('/<string:id>/images', 'get_vn_images', self.get_vn_images, methods=['GET'])
        self.bp.add_url_rule('/<string:id>/images/<string:image_id>', 'get_vn_image', self.get_vn_image, methods=['GET'])
        self.bp.add_url_rule('/<string:id>/images', 'upload_vn_images', self.upload_vn_images, methods=['POST'])
        self.bp.add_url_rule('/<string:id>/images', 'update_vn_images', self.update_vn_images, methods=['PUT'])
        self.bp.add_url_rule('/<string:id>/images/<string:image_id>', 'update_vn_image', self.update_vn_image, methods=['PUT'])
        self.bp.add_url_rule('/<string:id>/images', 'delete_vn_images', self.delete_vn_images, methods=['DELETE'])
        self.bp.add_url_rule('/<string:id>/images/<string:image_id>', 'delete_vn_image', self.delete_vn_image, methods=['DELETE'])
        self.bp.add_url_rule('/<string:id>/savedatas', 'get_vn_savedatas', self.get_vn_savedatas, methods=['GET'])
        self.bp.add_url_rule('/<string:id>/savedatas/<string:savedata_id>', 'get_vn_savedata', self.get_vn_savedata, methods=['GET'])
        self.bp.add_url_rule('/<string:id>/savedatas', 'upload_vn_savedatas', self.upload_vn_savedatas, methods=['POST'])
        self.bp.add_url_rule('/<string:id>/savedatas', 'delete_vn_savedatas', self.delete_vn_savedatas, methods=['DELETE'])
        self.bp.add_url_rule('/<string:id>/savedatas/<string:savedata_id>', 'delete_vn_savedata', self.delete_vn_savedata, methods=['DELETE'])

    def delete_resources(self):
        task = delete_vns_task.delay()
        return jsonify({"task_id": task.id}), 202

    def delete_resource(self, id):
        task = delete_vns_task.delay(id)
        return jsonify({"task_id": task.id}), 202

    def get_vn_images(self, id):
        task = get_images_task.delay('vn', id)
        return jsonify({"task_id": task.id}), 202

    def get_vn_image(self, id, image_id):
        format = request.args.get('format', default='file', type=str)
        if format == 'file':
            image_path = get_image_path('vn', id, image_id)
            if not image_path:
                abort(400, 'Invalid image URL')
            return send_file(image_path, mimetype='image/jpeg')

        task = get_images_task.delay('vn', id, image_id)
        return jsonify({"task_id": task.id}), 202

    def upload_vn_images(self, id):
        if 'files' not in request.files:
            return jsonify({"error": "No file part"}), 400
        files = request.files.getlist('files')
        file_data = [{'filename': file.filename, 'content': file.read()} for file in files]
        task = upload_images_task.delay('vn', id, file_data)
        return jsonify({"task_id": task.id}), 202

    def update_vn_images(self, id):
        task = update_images_task.delay('vn', id)
        return jsonify({"task_id": task.id}), 202

    def update_vn_image(self, id, image_id):
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400
        file = request.files['file']
        file_data = {'filename': file.filename, 'content': file.read()}
        task = update_images_task.delay('vn', id, image_id, file_data)
        return jsonify({"task_id": task.id}), 202

    def delete_vn_images(self, id):
        task = delete_images_task.delay('vn', id)
        return jsonify({"task_id": task.id}), 202

    def delete_vn_image(self, id, image_id):
        task = delete_images_task.delay('vn', id, image_id)
        return jsonify({"task_id": task.id}), 202

    def get_vn_savedatas(self, id):
        format = request.args.get('format', default='file', type=str)
        if format == 'file':
            savedatas = get_savedatas(vnid=id)
            if not savedatas:
                abort(404, description="No SaveData found for this VN")
            memory_file = BytesIO()
            with zipfile.ZipFile(memory_file, 'w') as zf:
                for savedata in savedatas:
                    savedata_id = savedata['id']
                    savedata_filename = savedata['filename']
                    savedata_path = get_savedata_path(id, savedata_id)
                    if savedata_path:
                        zf.write(savedata_path, savedata_filename)
            memory_file.seek(0)
            return send_file(memory_file, as_attachment=True, download_name=f"{id}.zip")

        task = get_savedatas_task.delay('vn', id)
        return jsonify({"task_id": task.id}), 202

    def get_vn_savedata(self, id, savedata_id):
        format = request.args.get('format', default='file', type=str)
        if format == 'file':
            savedata = get('savedata', savedata_id)
            savedata_path = get_savedata_path(id, savedata_id)
            if not savedata or not savedata_path:
                abort(400, 'Invalid file URL')
            return send_file(savedata_path, as_attachment=True, download_name=savedata.filename)

        task = get_savedatas_task.delay('vn', id, savedata_id)
        return jsonify({"task_id": task.id}), 202

    def upload_vn_savedatas(self, id):
        files = request.files.getlist('files')

        if not files or all(file.filename == '' for file in files):
            abort(400, description="No selected file")

        to_datetime = lambda ts: datetime.fromtimestamp(int(ts) / 1000.0, tz=timezone.utc) if ts else datetime.now(timezone.utc)

        serializable_files = [
            {
                'filename': file.filename,
                'content': file.read(),
                'last_modified': to_datetime(request.form.get(f'last_modified_{file.filename}'))
            } for file in files
        ]

        task = upload_savedatas_task.delay(id, serializable_files)
        return jsonify({"task_id": task.id}), 202

    def delete_vn_savedatas(self, id):
        task = delete_savedatas_task.delay('vn', id)
        return jsonify({"task_id": task.id}), 202

    def delete_vn_savedata(self, id, savedata_id):
        task = delete_savedatas_task.delay('vn', id, savedata_id)
        return jsonify({"task_id": task.id}), 202