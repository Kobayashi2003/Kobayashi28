import io
import os

from flask import current_app

from api import celery
from api.database import exists, create, next_image_id
from api.utils import convert_img_to_jpg

@celery.task(bind=True)
def upload_images_task(self, upload_type, id, files):
    self.update_state(state='PROGRESS', meta={'status': 'Checking model existence...'})
    if not exists(upload_type, id):
        return {"status": "NOT_FOUND", "result": None}

    self.update_state(state='PROGRESS', meta={'status': 'Processing images...'})

    upload_results = {}
    upload_folder = current_app.config['IMAGE_VN_FOLDER'] if upload_type == 'vn' else current_app.config['IMAGE_CHARACTER_FOLDER']
    if not os.path.exists(upload_folder): os.makedirs(upload_folder)

    for file_data in files:
        filename = file_data['filename']
        file_content = io.BytesIO(file_data['content'])

        try:
            success, result = convert_img_to_jpg(file_content)
            if not success:
                raise ValueError(f"Failed to convert {filename} to JPG")

            new_id = next_image_id(upload_type)

            image_path = os.path.join(upload_folder, f"{new_id}.jpg")
            with open(image_path, 'wb') as f:
                f.write(result.getvalue())

            create(
                type=f"{upload_type}_image",
                id=new_id,
                data={
                    f"{upload_type}_id": id,
                    "image_type": "u"
                }
            )

            upload_results[filename] = True

        except Exception as exc:
            # upload_results[filename] = str(exc)
            upload_results[filename] = False
            # If the image was saved but database entry failed, remove the saved file
            if 'image_path' in locals() and os.path.exists(image_path):
                os.remove(image_path)

    return {"status": "SUCCESS", "result": upload_results}
