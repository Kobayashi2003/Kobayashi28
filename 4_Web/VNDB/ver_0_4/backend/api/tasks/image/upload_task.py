from typing import Any, List, Dict, Union
from celery import Task

import io
import os

from api import celery
from api.database import create_upload_image, delete_image
from api.utils import convert_img_to_jpg, get_image_folder

@celery.task(bind=True)
def upload_images_task(self: Task, resource_type: str, resource_id: str, files: List[Dict]) -> Dict[str, Any]:

    self.update_state(state='PROGRESS', meta={'status': 'Processing images...'})

    upload_results: Dict[str, Union[bool, str]] = {}
    upload_folder = get_image_folder(resource_type)
    try:
        os.makedirs(upload_folder, exist_ok=True)
    except Exception as e:
        return {"status": "ERROR", "result": str(e)}

    for file_data in files:
        try:
            filename = file_data.get('filename', '')
            file_content = io.BytesIO(file_data.get('content', b''))
            if not file_content:
                raise ValueError(f"Failed to read content of {filename}")

            # Convert image to JPG format
            success, result = convert_img_to_jpg(file_content)
            if not success:
                raise ValueError(f"Failed to convert {filename} to JPG")

            # Create image record in database
            image = create_upload_image(resource_type, resource_id, {'image_type': 'u'})
            if not image:
                raise ValueError(f"Failed to create image for {filename}")

            image_id = image.id
            image_path = os.path.join(upload_folder, f"{image_id}.jpg")

            # Save the converted image to file
            with open(image_path, 'wb') as f:
                f.write(result.getvalue())

            upload_results[filename] = True
        except Exception as exc:
            # Clean up in case of failure
            if 'image_id' in locals() and image_id is not None:
                delete_image(resource_type, resource_id, image_id)
            if 'image_path' in locals() and os.path.exists(image_path):
                os.remove(image_path)
            upload_results[filename] = str(exc)

    return {"status": "SUCCESS", "result": upload_results}