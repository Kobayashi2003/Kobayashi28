import re
import zipfile
from io import BytesIO

from flask import request, abort, send_file
from . import savedata_bp
from api.database import get, get_savedatas
from api.utils.convert import convert_url_to_savedata_path
from api.utils.convert import convert_id_to_savedata_path
from api.utils.check import is_valid_id

@savedata_bp.route('/<string:id>', methods=['GET'])
def serve_savedata(id):

    if not is_valid_id(id, valid_letters=['v', 's']):
        abort(400, description="Invalid ID")

    if re.match(r'^s\d+$', id):
        savedata = get('savedata', id)
        if savedata is None:
            abort(404, description="SaveData not found")

        savedata_path = convert_url_to_savedata_path(request.url)

        if savedata_path is None:
            abort(400, description="Invalid savedata URL")

        return send_file(savedata_path, as_attachment=True, download_name=savedata.filename)

    elif re.match(r'^v\d+$', id):
        savedatas = get_savedatas(vnid=id)
        if not savedatas:
            abort(404, description="No SaveData found for this VN")

        memory_file = BytesIO()
        with zipfile.ZipFile(memory_file, 'w') as zf:
            for savedata in savedatas:
                savedata_id = savedata['id']
                savedata_filename = savedata['filename']
                savedata_path = convert_id_to_savedata_path(savedata_id)
                if savedata_path:
                    zf.write(savedata_path, savedata_filename)
        memory_file.seek(0)

        return send_file(memory_file, as_attachment=True, download_name=f"{id}.zip")

    else:
        abort(400, description="Invalid ID")