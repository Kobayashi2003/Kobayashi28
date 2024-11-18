from typing import Union, Dict, Optional

from api import celery
from api.database import exists, delete_image, delete_images 

@celery.task(bind=True)
def delete_images_task(self, resource_type: str, resource_id: str, image_id: Optional[str] = None) -> Dict[str, Union[str, Union[bool, int]]]:
    self.update_state(state='PROGRESS', meta={'status': 'Checking resource existence...'})
    if not exists(resource_type, resource_id):
        return {"status": "NOT_FOUND", "result": None}

    if image_id:
        self.update_state(state='PROGRESS', meta={'status': 'Deleting single image...'})
        if not exists(f"{resource_type}_image", image_id):
            return {"status": "NOT_FOUND", "result": None}
        
        result = delete_image(resource_type, resource_id, image_id)
        return {"status": "SUCCESS", "result": result}
    else:
        self.update_state(state='PROGRESS', meta={'status': 'Deleting all images...'})
        deleted_count = delete_images(resource_type, resource_id)
        return {"status": "SUCCESS", "result": deleted_count}