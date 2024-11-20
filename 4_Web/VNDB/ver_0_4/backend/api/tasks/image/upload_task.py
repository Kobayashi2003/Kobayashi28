from typing import Any, List, Dict, Union
from celery import Task
from sqlalchemy.exc import SQLAlchemyError

import io
import os

from api import celery
from api.database import create_upload_image, delete_image
from api.utils import convert_img_to_jpg, get_image_folder

@celery.task(bind=True)
def upload_images_task(
    self: Task, 
    resource_type: str, 
    resource_id: str, 
    files: List[Dict]
) -> Dict[str, Any]:
    """
    Celery task to upload and process multiple images for a given resource.

    This task processes multiple image files, creates database records, and saves the files.
    It updates its state during execution and returns the result of the upload operation.

    Args:
        self (Task): The Celery task instance (automatically injected by Celery).
        resource_type (str): The type of resource (e.g., 'vn', 'character').
        resource_id (str): The ID of the resource.
        files (List[Dict]): List of dictionaries containing file information.

    Returns:
        Dict[str, Any]: A dictionary containing the status and result of the upload operation.
        The structure is as follows:
        {
            "status": str,  # "SUCCESS" or "ERROR"
            "result": Dict[str, Union[bool, str]]  # Upload results for each file
        }

    Raises:
        SQLAlchemyError: If there's an issue with the database operation.
        OSError: If there's an issue with file operations.
        These exceptions are handled within the task.

    Note:
        - The task updates its state to 'PROGRESS' during execution.
        - For each file, it converts the image to JPG, creates a database record, and saves the file.
        - In case of failure for a specific file, it cleans up by deleting the record and file.
    """

    self.update_state(state='PROGRESS', meta={'status': 'Processing images...'})

    upload_results: Dict[str, Union[bool, str]] = {}
    upload_folder = get_image_folder(resource_type)
    os.makedirs(upload_folder, exist_ok=True)

    try:
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
    except (SQLAlchemyError, OSError) as e:
        print(f"Error in upload_images_task: {str(e)}")
        return {"status": "ERROR", "result": f"An error occurred during image upload: {str(e)}"}