from typing import Union, Dict, Optional
from celery import Task

from api import celery
from api.database import delete_image, delete_images, convert_model_to_dict

@celery.task(bind=True)
def delete_images_task(
    self: Task,
    resource_type: str,
    resource_id: str,
    image_id: Optional[str] = None
) -> Dict[str, Union[str, Union[Dict, int, None]]]:

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
    except Exception as e:
        return {"status": "ERROR", "result": str(e)}