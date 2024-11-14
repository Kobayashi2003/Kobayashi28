from api import celery
from api.database import get_image
from api.utils import convert_imgpath_to_imgid 

@celery.task(bind=True)
def get_image_task(self, get_type, id):
    self.update_state(state='PROGRESS', meta={'status': 'Retrieving image...'})

    image_data = get_image(get_type, id)
    if 'path' in image_data:
        image_data['id'] = convert_imgpath_to_imgid(image_data['path'])
        del image_data['path']

    return {
        "status": "SUCCESS" if image_data else "NOT_FOUND",
        "result": image_data if image_data else None
    }
        