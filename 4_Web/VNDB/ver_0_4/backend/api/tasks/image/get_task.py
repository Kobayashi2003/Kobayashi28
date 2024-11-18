from typing import Optional

from api import celery
from api.database import get_image, get_images, exists
from api.utils import convert_imgpath_to_imgid

@celery.task(bind=True)
def get_images_task(self, resource_type: str, resource_id: str, image_id: Optional[str] = None):
    self.update_state(state='PROGRESS', meta={'status': 'Checking resource existence...'})
    if not exists(resource_type, resource_id):
        return {"status": "NOT_FOUND", "result": None}

    self.update_state(state='PROGRESS', meta={'status': 'Retrieving image(s)...'})

    if image_id:
        # Retrieve a specific image
        image_data = get_image(resource_type, resource_id, image_id)
        if image_data and 'path' in image_data:
            image_data['id'] = convert_imgpath_to_imgid(image_data['path'])
            del image_data['path']
        return {
            "status": "SUCCESS" if image_data else "NOT_FOUND",
            "result": image_data if image_data else None
        }
    else:
        # Retrieve all images for the resource
        images_data = get_images(resource_type, resource_id)
        for image in images_data:
            if 'path' in image:
                image['id'] = convert_imgpath_to_imgid(image['path'])
                del image['path']
        return {
            "status": "SUCCESS" if images_data else "NOT_FOUND",
            "result": images_data if images_data else None
        }