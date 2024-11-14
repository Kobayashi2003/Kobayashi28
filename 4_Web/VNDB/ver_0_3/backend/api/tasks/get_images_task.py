from api import celery
from api.database import exists, get_images
from api.utils import convert_imgpath_to_imgid

@celery.task(bind=True)
def get_images_task(self, get_type, id):
    self.update_state(state='PROGRESS', meta={'status': 'Checking model existence...'})
    if not exists(get_type, id):
        return {"status": "NOT_FOUND", "result": None}

    self.update_state(state='PROGRESS', meta={'status': 'Retrieving images...'})
    images_data = get_images(get_type, id)

    # Convert path to id and remove path from the result
    for image in images_data:
        if 'path' in image:
            image['id'] = convert_imgpath_to_imgid(image['path'])
            del image['path']

    return {
        "status": "SUCCESS" if any(images_data) else "NOT_FOUND",
        "result": images_data if any(images_data) else None
    }