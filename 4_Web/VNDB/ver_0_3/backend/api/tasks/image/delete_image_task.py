from typing import Union, Dict

from api import celery
from api.database import exists, delete_image 

@celery.task(bind=True)
def delete_image_task(self, delete_type: str, id: str) -> Dict[str, Union[str, bool]]:
    self.update_state(state='PROGRESS', meta={'status': 'Checking image existence...'})
    if not exists(f"{delete_type}_image", id):
        return {"status": "NOT_FOUND", "result": None}

    self.update_state(state='PROGRESS', meta={'status': 'Deleting image...'})
    
    result = delete_image(delete_type, id)

    return {"status": "SUCCESS", "result": result}