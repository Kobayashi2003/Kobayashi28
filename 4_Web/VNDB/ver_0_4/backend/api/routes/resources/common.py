import zipfile
from io import BytesIO

from flask import send_file, abort

from api.database import get_savedatas, get_images, get
from api.utils import get_image_path, get_savedata_path

def get_savedata_file(savedata_id):
    savedata = get('savedata', savedata_id)
    savedata_path = get_savedata_path(savedata_id)
    if not savedata or not savedata_path:
        abort(404, description="SaveData not found")
    return send_file(savedata_path, as_attachment=True, download_name=savedata.filename)

def get_image_file(resource_type, image_id):
    image_path = get_image_path(resource_type, image_id)
    if not image_path:
        abort(404, description="Image not found")
    return send_file(image_path, mimetype='image/jpeg')

def create_savedatas_zip(vnid):
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

def create_images_zip(resource_type, resource_id):
    images = get_images(resource_type, resource_id)
    if not images:
        abort(404, description=f"No images found for this {resource_type}")
    memory_file = BytesIO()
    with zipfile.ZipFile(memory_file, 'w') as zf:
        for image in images:
            image_id = image.id
            image_filename = f"{image_id}.jpg"
            image_path = get_image_path(resource_type, image_id)
            if image_path:
                zf.write(image_path, image_filename)
    memory_file.seek(0)
    return send_file(memory_file, as_attachment=True, download_name=f"{resource_id}_images.zip")
