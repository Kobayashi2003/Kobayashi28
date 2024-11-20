from typing import Optional, Dict, Union, List
from celery import Task
from sqlalchemy.exc import SQLAlchemyError

from api import celery
from api.database import get_image, get_images, convert_model_to_dict

@celery.task(bind=True)
def get_images_task(self: Task,
    resource_type: str,
    resource_id: str,
    image_id: Optional[str] = None
) -> Dict[str, Union[str, Union[Dict, List[Dict], None]]]:
    """
    Celery task to retrieve one or all images associated with a resource.

    This task can retrieve either a single image (if image_id is provided) or all images
    associated with a specific resource. It updates its state during execution and
    returns the result of the retrieval operation.

    Args:
        self (Task): The Celery task instance (automatically injected by Celery).
        resource_type (str): The type of resource ('vn' or 'character').
        resource_id (str): The ID of the resource.
        image_id (Optional[str], optional): The ID of the specific image to retrieve.
            If None, all images for the resource will be retrieved. Defaults to None.

    Returns:
        Dict[str, Union[str, Union[Dict, List[Dict], None]]]: A dictionary containing the status
        of the operation and its result. The structure is as follows:
        {
            "status": str,  # "SUCCESS", "NOT_FOUND", or "ERROR"
            "result": Union[Dict, List[Dict], None]  # Image data or list of image data
        }

    Raises:
        SQLAlchemyError: If there's an issue with the database operation.
        This exception is handled by Celery's error handling mechanisms.

    Note:
        - The task updates its state to 'PROGRESS' during execution.
        - For single image retrieval, it returns the image data if found.
        - For all images retrieval, it returns a list of image data.
        - The image data is converted to a dictionary format using convert_model_to_dict.
    """

    self.update_state(state='PROGRESS', meta={'status': 'Retrieving image(s)...'})

    try:
        if image_id:
            image = get_image(resource_type, resource_id, image_id)
            return {
                "status": "SUCCESS" if image else "NOT_FOUND",
                "result": convert_model_to_dict(image) if image else None
            }
        else:
            images = get_images(resource_type, resource_id)
            return {
                "status": "SUCCESS" if images else "NOT_FOUND",
                "result": [convert_model_to_dict(image) for image in images] if images else []
            }
    except SQLAlchemyError as e:
        # Log the error or handle it as appropriate for your application
        print(f"Database error in get_images_task: {str(e)}")
        return {
            "status": "ERROR",
            "result": f"An error occurred while retrieving image(s): {str(e)}"
        }