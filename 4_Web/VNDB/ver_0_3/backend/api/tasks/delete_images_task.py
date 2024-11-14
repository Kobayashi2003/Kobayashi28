from typing import Union, Dict

from api import celery
from api.database import exists, delete_images

@celery.task(bind=True)
def delete_images_task(self, delete_type: str, id: str) -> Dict[str, Union[str, int]]:
    self.update_state(state='PROGRESS', meta={'status': 'Checking model existence...'})
    if not exists(delete_type, id):
        return {"status": "NOT_FOUND", "result": None}

    self.update_state(state='PROGRESS', meta={'status': 'Deleting images...'})
    
    deleted_count = delete_images(delete_type, id)

    return {"status": "SUCCESS", "result": deleted_count}
