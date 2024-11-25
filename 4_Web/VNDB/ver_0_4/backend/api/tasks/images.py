from typing import Dict, List, Any

import io
import os

from api import celery
from api.database import (
    get, create_image, create_upload_image,
    get_image, get_images, delete_image, delete_images,
    convert_model_to_dict, extract_images
)
from api.utils import (
    download_image, download_images, 
    get_image_folder, convert_img_to_jpg, 
    convert_imgurl_to_imgid
)
from .common import error_handler

@error_handler
def _delete_image_task(resource_type: str, resource_id: str, image_id: str) -> Dict[str, Any]:
    result = delete_image(resource_type, resource_id, image_id)
    return {
        "status": "SUCESS" if result else "NOT_FOUND",
        "result": convert_model_to_dict(result) if result else None
    }

@error_handler
def _delete_images_task(resource_type: str, resource_id: str) -> Dict[str, Any]:
    deleted_count = delete_images(resource_type, resource_id)
    return {
        "status": "SUCCESS" if deleted_count else "NOT_FOUND",
        "result": deleted_count
    }

@error_handler
def _get_image_task(resource_type: str, resource_id: str, image_id: str) -> Dict[str, Any]:
    image = get_image(resource_type, resource_id, image_id)
    return {
        "status": "SUCCESS" if image else "NOT_FOUND",
        "result": convert_model_to_dict(image) if image else None
    }

@error_handler
def _get_images_task(resource_type: str, resource_id: str) -> Dict[str, Any]:
    images = get_images(resource_type, resource_id)
    return {
        "status": "SUCCESS" if images else "NOT_FOUND",
        "result": [convert_model_to_dict(image) for image in images] if images else []
    }

@error_handler
def _upload_image_task(resource_type: str, resource_id: str, file: Dict[str, Any]) -> Dict[str, Any]:
    filename = file['filename']
    if not filename:
        raise ValueError("Filename is missing")

    file_content = io.BytesIO(file['content'])
    if not file_content:
        raise ValueError(f"Failed to read content of {filename}")

    success, result = convert_img_to_jpg(file_content)
    if not success:
        raise ValueError(f"Failed to convert {filename} to JPG")

    image = create_upload_image(resource_type, resource_id, {'image_type': 'u'})
    if not image:
        raise ValueError(f"Failed to create image for {filename}")

    image_id = image.id
    image_path = os.path.join(get_image_folder(resource_type), f"{image_id}.jpg")

    with open(image_path, 'wb') as f:
        f.write(result.getvalue())
        
    return {
        "status": "SUCESS",
        "result": convert_model_to_dict(image)
    }

@error_handler
def _upload_images_task(resource_type: str, resource_id: str, files: List[Dict]) -> Dict[str, Any]:
    upload_results = {}
    for file in files:
        filename = file['filename']
        if not filename:
            raise ValueError("Filename is missing")
        result = _upload_image_task(resource_type, resource_id, filename, file)
        upload_results[filename] = True if result.get('status') == 'SUCESS' else False
    
    return {
        'status': 'ALL SUCCESS' if all(upload_results.values()) else 'SOME FAILURE',
        'result': upload_results
    }

@error_handler
def _update_image_task(resource_type: str, resource_id: str, image_id: str) -> Dict[str, Any]:
    resource_data = get(resource_type, resource_id)
    if not resource_data:
        return {"status": "NOT_FOUND", "result": None}

    urls_info = extract_images(resource_type, resource_data)
    for url_info in urls_info:
        url, type = next(iter(url_info.items()))
        if convert_imgurl_to_imgid(url) == image_id:
            url_to_download = url
            image_type = type
            break
    else:
        return {"status": "IMAGE NOT FOUND", "result": None}

    download_folder = get_image_folder(resource_type)
    download_result = download_image(url_to_download, download_folder)

    if not download_result:
        return {"status": "DOWNLOAD FAILED", "result": None}

    delete_image(resource_type, resource_id, image_id)
    image = create_image(resource_type, resource_id, image_id, {"image_type": image_type})

    return {
        'status': 'SUCCESS' if image else "FAILED",
        'result': convert_model_to_dict(image) if image else None 
    }

@error_handler
def _update_images_task(resource_type: str, resource_id: str) -> Dict[str, Any]:
    resource_data = get(resource_type, resource_id)
    if not resource_data:
        return {"status": "NOT_FOUND", "result": None}

    urls_info = extract_images(resource_type, resource_data)
    urls_to_download = [next(iter(url_info.keys())) for url_info in urls_info]
    if not urls_to_download:
        return {"status": "NO IMAGES FOUND", "result": None}

    download_folder = get_image_folder(resource_type)
    download_results = download_images(urls_to_download, download_folder)

    successful_downloads = [url for url, success in download_results.items() if success]
    if not successful_downloads:
        return {"status": "ALL DOWNLOADS FAILED", "result": download_results}

    for url in successful_downloads:
        get_image_type = lambda url: next(info_dict[url] for info_dict in urls_info if url in info_dict)
        try:
            image_id = convert_imgurl_to_imgid(url)
            image_data = {
                f"{resource_type}_id": resource_id,
                "image_type": get_image_type(url)
            }

            # Delete existing image and create a new one
            delete_image(resource_type, resource_id, image_id)
            image = create_image(resource_type, resource_id, image_id, image_data)

            if not image:
                download_results[url] = False
        except Exception as e:
            download_results[url] = False
            print(f"Error processing image {url}: {str(e)}")

    return {
        "status": "ALL IMAGES UPDATED" if all(download_results.values()) else "SOME IMAGES FAILED",
        "result": download_results
    }

@celery.task
def delete_image_task(*args, **kwargs) -> Dict[str, Any]:
    return _delete_image_task(*args, **kwargs)

@celery.task
def delete_images_task(*args, **kwargs) -> Dict[str, Any]:
    return _delete_images_task(*args, **kwargs)

@celery.task
def get_image_task(*args, **kwargs) -> Dict[str, Any]:
    return _get_image_task(*args, **kwargs)

@celery.task
def get_images_task(*args, **kwargs) -> Dict[str, Any]:
    return _get_images_task(*args, **kwargs)

@celery.task
def upload_image_task(*args, **kwargs) -> Dict[str, Any]:
    return _upload_image_task(*args, **kwargs)

@celery.task
def upload_images_task(*args, **kwargs) -> Dict[str, Any]:
    return _upload_images_task(*args, **kwargs)

@celery.task
def update_image_task(*args, **kwargs) -> Dict[str, Any]:
    return _update_image_task(*args, **kwargs)

@celery.task
def update_images_task(*args, **kwargs) -> Dict[str, Any]:
    return _update_images_task(*args, **kwargs)