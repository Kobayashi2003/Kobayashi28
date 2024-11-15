from typing import Union, List, Dict

from api import celery
from api.database import exists, create
from api.database.models import VN, Character

@celery.task(bind=True)
def upload_images_task(self, upload_type, id, files):
    ...

