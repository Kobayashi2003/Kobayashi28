from typing import Dict, List, Any
from flask import current_app
from imgserve import celery
from imgserve.database import create, update, delete
from imgserve.utils import download_images 
from .common import SUCCESS, FAILED 

@celery.task
def create_image_task(type: str, id: int) -> Dict[str, str]:
    try:
        result = create(type, id)
    except Exception as e:
        return {'status': 'ERROR', 'results': str(e)}
    if not result:
        return FAILED
    return SUCCESS

@celery.task
def update_image_task(type: str, id: int) -> Dict[str, str]:
    try:
        result = update(type, id)
    except Exception as e:
        return {'status': 'ERROR', 'results': str(e)}
    if not result:
        return FAILED
    return SUCCESS

@celery.task
def delete_image_task(type: str, id: int) -> Dict[str, str]:
    try:
        result = delete(type, id)
    except Exception as e:
        return {'status': 'ERROR', 'results': str(e)}
    if not result:
        return FAILED
    return SUCCESS

@celery.task
def download_images_task(urls: List[str]) -> Dict[str, Any]:
    try:
        image_folder = current_app.config['IMAGE_FOLDER']
        results = download_images(urls, image_folder)
    except Exception as e:
        return {'status': 'ERROR', 'results': str(e)}
    return {'status': 'SUCCESS', 'results': results}
    