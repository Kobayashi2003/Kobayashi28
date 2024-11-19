from typing import Any, List, Dict, Union, Optional

import io
import os
from io import BytesIO

from celery import Task
from api import celery
from api.database import create_image, delete_image
from api.utils import convert_img_to_jpg, get_image_folder
from api.database import ImageModelType

@celery.task(bind=True)
def upload_images_task(self: Task, resource_type: str, resource_id: str, files: List[Dict]) -> Dict[str, Any]:
    """
    Celery task to upload and process multiple images for a given resource.

    Args:
        self (Task): The Celery task instance.
        resource_type (str): The type of resource (e.g., 'vn', 'character').
        resource_id (str): The ID of the resource.
        files (List[Dict]): List of dictionaries containing file information.

    Returns:
        Dict[str, Any]: A dictionary containing the task status and upload results.
    """
    self.update_state(state='PROGRESS', meta={'status': 'Processing images...'})

    upload_results: Dict[str, Union[bool, str]] = {}
    upload_folder: str = get_image_folder(resource_type)
    os.makedirs(upload_folder, exist_ok=True)

    for file_data in files:
        try:
            filename: str = file_data.get('filename', '')
            file_content: BytesIO = io.BytesIO(file_data.get('content', b''))
            if not file_content:
                raise ValueError(f"Failed to read content of {filename}")

            # Convert image to JPG format
            success, result = convert_img_to_jpg(file_content)
            if not success:
                raise ValueError(f"Failed to convert {filename} to JPG")

            # Create image record in database
            image: Optional[ImageModelType] = create_image(resource_type, resource_id, {'image_type': 'u'})
            if not image:
                raise ValueError(f"Failed to create image for {filename}")

            image_id: str = image.id
            image_path: str = os.path.join(upload_folder, f"{image_id}.jpg")

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