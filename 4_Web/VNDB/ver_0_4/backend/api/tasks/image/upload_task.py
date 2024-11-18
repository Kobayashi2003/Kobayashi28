import io
import os

from flask import current_app

from api import celery
from api.database import exists, create, next_image_id
from api.utils import convert_img_to_jpg

@celery.task(bind=True)
def upload_images_task(self, resource_type: str, resource_id: str, files: list):
    self.update_state(state='PROGRESS', meta={'status': 'Checking resource existence...'})
    if not exists(resource_type, resource_id):
        return {"status": "NOT_FOUND", "result": f"{resource_type.capitalize()} with id {resource_id} not found"}

    self.update_state(state='PROGRESS', meta={'status': 'Processing images...'})

    upload_results = {}
    upload_folder = current_app.config[f'IMAGE_{resource_type.upper()}_FOLDER']
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    for file_data in files:
        filename = file_data['filename']
        file_content = io.BytesIO(file_data['content'])

        try:
            success, result = convert_img_to_jpg(file_content)
            if not success:
                raise ValueError(f"Failed to convert {filename} to JPG")

            new_id = next_image_id(resource_type)

            image_path = os.path.join(upload_folder, f"{new_id}.jpg")
            with open(image_path, 'wb') as f:
                f.write(result.getvalue())

            create(
                type=f"{resource_type}_image",
                id=new_id,
                data={
                    f"{resource_type}_id": resource_id,
                    "image_type": "u"
                }
            )

            upload_results[filename] = True

        except Exception as exc:
            upload_results[filename] = False
            # If the image was saved but database entry failed, remove the saved file
            if 'image_path' in locals() and os.path.exists(image_path):
                os.remove(image_path)

    return {"status": "SUCCESS", "result": upload_results}