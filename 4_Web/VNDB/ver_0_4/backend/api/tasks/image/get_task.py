from typing import Optional, Dict, Union, List
from celery import Task

from api import celery
from api.database import get_image, get_images, convert_model_to_dict

@celery.task(bind=True)
def get_images_task(self: Task,
    resource_type: str,
    resource_id: str,
    image_id: Optional[str] = None
) -> Dict[str, Union[str, Union[Dict, List[Dict], None]]]:

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
    except Exception as e:
        return {"status": "ERROR", "result": str(e)}