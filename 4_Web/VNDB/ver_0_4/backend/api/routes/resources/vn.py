from .base import BaseResourceBlueprint
from flask import jsonify, request, abort, send_file
from io import BytesIO
import zipfile
from datetime import datetime, timezone

from api.database import get_savedatas, get
from api.utils import get_image_path, get_savedata_path

from api.tasks.image import (
    get_images_task, upload_images_task, update_images_task, delete_images_task
)
from api.tasks.savedata import (
    get_savedatas_task, upload_savedatas_task, delete_savedatas_task
)

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

    # def update_resources(self):
    #     ...

    # def update_resource(self, id):
    #     ...

    def get_vn_images(self, vnid):
        task = get_images_task.delay('vn', vnid)
        return jsonify({"task_id": task.id}), 202

    def get_vn_image(self, vnid, image_id):
        format = request.args.get('format', default='file', type=str)
        if format == 'file':
            image_path = get_image_path('vn', image_id)
            if not image_path:
                abort(400, 'Invalid image URL')
            return send_file(image_path, mimetype='image/jpeg')

        task = get_images_task.delay('vn', vnid, image_id)
        return jsonify({"task_id": task.id}), 202

    def upload_vn_images(self, vnid):
        if 'files' not in request.files:
            return jsonify({"error": "No file part"}), 400
        files = request.files.getlist('files')
        file_data = [{'filename': file.filename, 'content': file.read()} for file in files]

        task = upload_images_task.delay('vn', vnid, file_data)
        return jsonify({"task_id": task.id}), 202

    def update_vn_images(self, vnid):
        task = update_images_task.delay('vn', vnid)
        return jsonify({"task_id": task.id}), 202

    def update_vn_image(self, vnid, image_id):
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400
        file = request.files['file']
        file_data = {'filename': file.filename, 'content': file.read()}

        task = update_images_task.delay('vn', vnid, image_id, file_data)
        return jsonify({"task_id": task.id}), 202

    def delete_vn_images(self, vnid):
        task = delete_images_task.delay('vn', vnid)
        return jsonify({"task_id": task.id}), 202

    def delete_vn_image(self, vnid, image_id):
        task = delete_images_task.delay('vn', vnid, image_id)
        return jsonify({"task_id": task.id}), 202

    def get_vn_savedatas(self, vnid):
        format = request.args.get('format', default='file', type=str)
        if format == 'file':
            savedatas = get_savedatas(vnid)
            if not savedatas:
                abort(404, description="No SaveData found for this VN")
            memory_file = BytesIO()
            with zipfile.ZipFile(memory_file, 'w') as zf:
                for savedata in savedatas:
                    savedata_id = savedata.id
                    savedata_filename = savedata.filename
                    savedata_path = get_savedata_path(savedata_id)
                    if savedata_path:
                        zf.write(savedata_path, savedata_filename)
            memory_file.seek(0)
            return send_file(memory_file, as_attachment=True, download_name=f"{vnid}.zip")

        task = get_savedatas_task.delay(vnid)
        return jsonify({"task_id": task.id}), 202

    def get_vn_savedata(self, vnid, savedata_id):
        format = request.args.get('format', default='file', type=str)
        if format == 'file':
            savedata = get('savedata', savedata_id)
            savedata_path = get_savedata_path(savedata_id)
            if not savedata or not savedata_path:
                abort(400, 'Invalid file URL')
            return send_file(savedata_path, as_attachment=True, download_name=savedata.filename)

        task = get_savedatas_task.delay(vnid, savedata_id)
        return jsonify({"task_id": task.id}), 202

    def upload_vn_savedatas(self, vnid):
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

        task = upload_savedatas_task.delay(vnid, serializable_files)
        return jsonify({"task_id": task.id}), 202

    def delete_vn_savedatas(self, vnid):
        task = delete_savedatas_task.delay('vn', vnid)
        return jsonify({"task_id": task.id}), 202

    def delete_vn_savedata(self, vnid, savedata_id):
        task = delete_savedatas_task.delay('vn', vnid, savedata_id)
        return jsonify({"task_id": task.id}), 202

vn_bp = VNResourceBlueprint().blueprint

@vn_bp.route('/<string:vnid>/characters', methods=[])
def vc1(vnid: str): ...

@vn_bp.route('/<string:vnid>/characters/<string:charid>', methods=[])
def vc2(vnid: str, charid: str): ...

@vn_bp.route('/<string:vnid>/tags', methods=[])
def vt1(vnid: str): ...

@vn_bp.route('/<string:vnid>/tags/<string:tag_id>', methods=[])
def vt2(vnid: str, tag_id: str): ...

@vn_bp.route('/<string:vnid>/developers', methods=[])
def vd1(vnid: str): ...

@vn_bp.route('/<string:vnid>/deverlopers/<string:dev_id>', methods=[])
def vd2(vnid: str, dev_id: str): ...

@vn_bp.route('/<string:vnid>/staff', methods=[])
def vs1(vnid: str): ...

@vn_bp.route('/<string:vnid>/staff/<string:staff_id>', methods=[])
def vs2(vnid: str, staff_id): ...

@vn_bp.route('/<string:vnid>/traits', methods=[])
def vtr1(vnid: str): ...

@vn_bp.route('/<string:vnid>/traits/<string:trait_id>', methods=[])
def vtr2(vnid: str, trait_id: str): ...