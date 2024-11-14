from typing import Union, List, Dict

from flask import current_app

from api import celery
from api.database import get, exists, create, update, delete_image 
from api.database.models import VN, Character
from api.utils import extract_images, download_images, convert_imgurl_to_imgid

@celery.task(bind=True)
def update_images_task(self, update_type, id):
    self.update_state(state='PROGRESS', meta={'status': 'Checking model existence...'})
    if not exists(update_type, id):
        return {"status": "NOT_FOUND", "result": None}

    self.update_state(state='PROGRESS', meta={'status': 'Extracting image URLs...'})
    data: Union[VN, Character] = get(update_type, id)
    urls_info: List[Dict[str, str]] = extract_images(update_type, data)
    urls = [next(iter(url_info.keys())) for url_info in urls_info]
    urls_to_download = urls

    if not urls_to_download:
        return {"status": "SUCCESS", "result": {}}

    self.update_state(state='PROGRESS', meta={'status': 'Deleting old images...'})
    image_ids = [convert_imgurl_to_imgid(url) for url in urls]
    for image_id in image_ids:
        delete_image(update_type, image_id)

    get_image_type = lambda url: next(info_dict[url] for info_dict in urls_info if url in info_dict)

    self.update_state(state='PROGRESS', meta={'status': 'Downloading images...'})
    download_path = current_app.config['IMAGE_VN_FOLDER'] if update_type == 'vn' else current_app.config['IMAGE_CHARACTER_FOLDER']
    download_results = download_images(urls_to_download, download_path)

    self.update_state(state='PROGRESS', meta={'status': 'Updating database...'})

    successful_downloads = [url for url, success in download_results.items() if success]
    for url in successful_downloads:
        create(
            type=f"{update_type}_image",
            id=convert_imgurl_to_imgid(url),
            data= {
                f"{update_type}_id": id,
                "image_type": get_image_type(url)
            }
        )

    update(f"local_{update_type}", id, {"downloaded": True})

    return {"status": "SUCCESS", "result": download_results}
