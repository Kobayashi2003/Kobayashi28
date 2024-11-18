from typing import Optional, Union, List, Dict

import io
import os

from api import celery
from api.database import get_image, delete_image
from api.database import exists, update, create, get, models
from api.utils import extract_images, download_images, get_image_folder
from api.utils import convert_imgid_to_imgpath, convert_img_to_jpg, convert_imgurl_to_imgid

@celery.task(bind=True)
def update_images_task(self, resource_type: str, resource_id: str, image_id: Optional[str] = None, file: Optional[Dict] = None):
    self.update_state(state='PROGRESS', meta={'status': 'Checking resource existence...'})
    if not exists(resource_type, resource_id):
        return {"status": "NOT_FOUND", "result": f"{resource_type.capitalize()} with id {resource_id} not found"}

    if image_id:
        self.update_state(state='PROGRESS', meta={'status': 'Updating single image...'})
        return update_single_image(resource_type, resource_id, image_id, file)
    else:
        self.update_state(state='PROGRESS', meta={'status': 'Updating all images...'})
        return update_all_images(resource_type, resource_id)

def update_single_image(resource_type: str, resource_id: str, image_id: str, file: dict):
    
    if not exists(resource_type, resource_id):
        return {"status": "NOT_FOUND", "result": f"{resource_type.capitalize()} with id {resource_id} not found"}
    
    image_data = get_image(resource_type, resource_id, image_id)
    if not image_data:
        return {"status": "NOT_FOUND", "result": f"Image with id {image_id} not found for {resource_type} {resource_id}"}

    try:
        # Delete the original image file
        image_path = convert_imgid_to_imgpath(image_id)
        if image_path:
            os.remove(image_path)
        
        filename = file['filename']
        file_content = io.BytesIO(file['content'])

        # Convert and save the new image
        success, result = convert_img_to_jpg(file_content)
        if not success:
            raise ValueError(f"Failed to convert {filename} to JPG")

        with open(image_path, 'wb') as f:
            f.write(result.getvalue())

        # Update the image entry in the database
        update(
            type=f"{resource_type}_image",
            id=image_id,
            data={
                f"{resource_type}_id": resource_id,
                "image_type": "u"
            }
        )

        return {"status": "SUCCESS", "result": f"Image {filename} updated successfully for {resource_type} {resource_id}"}

    except Exception as e:
        # If an error occurs, ensure any partially created files are cleaned up
        if 'image_path' in locals() and os.path.exists(image_path):
            os.remove(image_path)
        return {"status": "ERROR", "result": str(e)}

def update_all_images(resource_type: str, resource_id: str):
    if not exists(resource_type, resource_id):
        return {"status": "NOT_FOUND", "result": f"{resource_type.capitalize()} with id {resource_id} not found"}

    data: Union[models.VN, models.Character] = get(resource_type, resource_id)
    urls_info: List[Dict[str, str]] = extract_images(resource_type, data)
    urls = [next(iter(url_info.keys())) for url_info in urls_info]
    urls_to_download = urls

    if not urls_to_download:
        return {"status": "SUCCESS", "result": {}}

    image_ids = [convert_imgurl_to_imgid(url) for url in urls]
    for image_id in image_ids:
        delete_image(resource_type, resource_id, image_id)

    get_image_type = lambda url: next(info_dict[url] for info_dict in urls_info if url in info_dict)

    download_path = get_image_folder(resource_type=resource_type)
    download_results = download_images(urls_to_download, download_path)

    successful_downloads = [url for url, success in download_results.items() if success]
    for url in successful_downloads:
        try:
            value_type = f"{resource_type}_image"
            value_id = convert_imgurl_to_imgid(url)
            value_data = {
                f"{resource_type}_id": resource_id,
                "image_type": get_image_type(url)
            }
            create(type=value_type, id=value_id, data=value_data)
        except Exception as e:
            download_results[url] = False
            file_path = os.path.join(download_path, f"{value_id}.jpg")
            if os.path.exists(file_path):
                os.remove(file_path)

    update(f"local_{resource_type}", resource_id, {"downloaded": True})

    return {"status": "SUCCESS", "result": download_results}