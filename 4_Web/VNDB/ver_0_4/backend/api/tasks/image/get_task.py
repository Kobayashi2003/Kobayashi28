from typing import Optional, Dict, Any, List
from celery import Task

from api import celery
from api.database import get_image, get_images, convert_model_to_dict
from api.database import ImageModelType

@celery.task(bind=True)
def get_images_task(
    self: Task,
    resource_type: str,
    resource_id: str,
    image_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Celery task to retrieve image(s) for a given resource.

    Args:
        self (Task): The Celery task instance.
        resource_type (str): The type of resource (e.g., 'vn', 'character').
        resource_id (str): The ID of the resource.
        image_id (Optional[str]): The specific image ID to retrieve, if any.

    Returns:
        Dict[str, Any]: A dictionary containing the task status and retrieved image(s) data.
    """
    self.update_state(state='PROGRESS', meta={'status': 'Retrieving image(s)...'})

    if image_id:
        # Retrieve a single image
        image: Optional[ImageModelType] = get_image(resource_type, resource_id, image_id)
        return {
            "status": "SUCCESS" if image else "NOT_FOUND",
            "result": convert_model_to_dict(image) if image else None
        }
    else:
        # Retrieve all images for the resource
        images: List[ImageModelType] = get_images(resource_type, resource_id)
        return {
            "status": "SUCCESS" if images else "NOT_FOUND",
            "result": [convert_model_to_dict(image) if image else None for image in images]
        }