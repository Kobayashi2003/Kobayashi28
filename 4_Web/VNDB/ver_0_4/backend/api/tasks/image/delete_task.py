from typing import Union, Dict, Optional, List
from celery import Task
from sqlalchemy.exc import SQLAlchemyError

from api import celery
from api.database import delete_image, delete_images, convert_model_to_dict

@celery.task(bind=True)
def delete_images_task(
    self: Task,
    resource_type: str,
    resource_id: str,
    image_id: Optional[str] = None
) -> Dict[str, Union[str, Union[Dict, int, None]]]:
    """
    Celery task to delete one or all images associated with a resource.

    This task can delete either a single image (if image_id is provided) or all images
    associated with a specific resource. It updates its state during execution and
    returns the result of the deletion operation.

    Args:
        self (Task): The Celery task instance (automatically injected by Celery).
        resource_type (str): The type of resource ('vn' or 'character').
        resource_id (str): The ID of the resource.
        image_id (Optional[str], optional): The ID of the specific image to delete.
            If None, all images for the resource will be deleted. Defaults to None.

    Returns:
        Dict[str, Union[str, Union[Dict, int, None]]]: A dictionary containing the status
        of the operation and its result. The structure is as follows:
        {
            "status": str,  # "SUCCESS", "NOT_FOUND", or "ERROR"
            "result": Union[Dict, int, str, None]  # Deleted image data, count of deleted images, or error message
        }

    Raises:
        SQLAlchemyError: If there's an issue with the database operation.
        This exception is handled by Celery's error handling mechanisms.

    Note:
        - The task updates its state to 'PROGRESS' during execution.
        - For single image deletion, it returns the deleted image data if successful.
        - For bulk deletion, it returns the count of deleted images.
        - The image data is converted to a dictionary format using convert_model_to_dict.
    """

    try:
        if image_id:
            self.update_state(state='PROGRESS', meta={'status': 'Deleting single image...'})
            result = delete_image(resource_type, resource_id, image_id)
            if not result:
                return {"status": "NOT_FOUND", "result": f"Image with id {image_id} not found for {resource_type} {resource_id}"}
            return {"status": "SUCCESS", "result": convert_model_to_dict(result)}
        else:
            self.update_state(state='PROGRESS', meta={'status': 'Deleting all images...'})
            deleted_count = delete_images(resource_type, resource_id)
            if not deleted_count:
                return {"status": "NOT_FOUND", "result": f"No images found for {resource_type} {resource_id}"}
            return {"status": "SUCCESS", "result": deleted_count}
    except SQLAlchemyError as e:
        # Log the error or handle it as appropriate for your application
        print(f"Database error in delete_images_task: {str(e)}")
        return {
            "status": "ERROR",
            "result": f"An error occurred while deleting image(s): {str(e)}"
        }