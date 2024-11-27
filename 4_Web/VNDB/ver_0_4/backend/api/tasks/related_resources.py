from typing import Dict, Any

from api import celery
from api.search import (
    search_resources_by_vnid, 
    search_resources_by_charid
)
from api.database import (
    exists, create, update, 
    get_images, create_image, 
    delete_image, delete_images,
    get_all_related, delete_all_related, 
    convert_model_to_dict
)
from api.utils import (
    convert_remote_to_local,
    convert_imgurl_to_imgid,
    get_image_folder,
    download_images
)
from .common import error_handler

@error_handler
def _get_related_characters_images_task(vnid: str) -> Dict[str, Any]:
    results = {}

    characters = get_all_related('vn', vnid, 'character')
    for char in characters:
        charid = char['id']
        images = get_images('character', charid)
        results[charid] = convert_model_to_dict(images[0]) if images else None

    return {
        'status': 'SUCCESS' if results else 'NOT_FOUND',
        'result': results
    }

@error_handler
def _update_related_characters_images_task(vnid: str) -> Dict[str, Any]:
    characters = get_all_related('vn', vnid, 'character')

    urls_to_download = {char['image']['url']: char['id'] 
        for char in characters if char.get('image') and char['image'].get('url')}
    if not urls_to_download:
        return {"status": "NOT_FOUND", "result": None}
    
    download_folder = get_image_folder('character')
    download_results = download_images(urls_to_download.keys(), download_folder)

    successful_downloads = [url for url, success in download_results.items() if success]

    for url in successful_downloads:
        try:
            charid = urls_to_download[url]
            image_id = convert_imgurl_to_imgid(url)
            image_data = {"character_id": charid, "image_type": 'ch'}

            delete_image('character', charid, image_id)
            image = create_image('character', charid, image_id, image_data)
            if not image:
                download_results = False
        except Exception as exc:
            download_results[url] = False

    return {
        "status": "SUCCESS" if successful_downloads else "FAILED",
        "result": download_results
    }

@error_handler
def _delete_related_characters_images_task(vnid: str) -> Dict[str, Any]:
    results = {}

    characters = get_all_related('vn', vnid, 'character')
    for char in characters:
        charid = char['id']
        deleted_count = delete_images('character', charid)
        results[charid] = deleted_count

    return {
        "status": 'SUCCESS' if results else 'NOT_FOUND',
        "result": results
    }

@error_handler
def _get_related_resources_task(resource_type: str, resource_id: str, related_resource_type: str) -> Dict[str, Any]:
    result = get_all_related(resource_type, resource_id, related_resource_type)
    return {
        'status': 'SUCCESS' if result else 'NOT_FOUND',
        'result': result if result else None
    }

@error_handler
def _search_related_resources_task(resource_type: str, resource_id: str, related_resource_type: str, response_size: str = 'small') -> Dict[str, Any]:
    
    if resource_type == 'vn':
        search_results = search_resources_by_vnid(resource_id, related_resource_type, response_size)
    elif resource_type == 'character':
        search_results = search_resources_by_charid(resource_id, related_resource_type, response_size)
    else:
        raise ValueError(f"Invalid resource_type: {resource_type}. Only 'vn' and 'character' are supported.")
    
    if not search_results or not isinstance(search_results, dict) or not search_results.get('results'):
        raise ValueError(f"No related {related_resource_type} found for {resource_type} {resource_id}")

    return {
        'status': 'SUCCESS' if search_results else 'NOT_FOUND',
        'result': search_results
    }

@error_handler
def _update_related_resources_task(resource_type: str, resource_id: str, related_resource_type: str) -> Dict[str, Any]:
    if resource_type == 'vn':
        related_data = search_resources_by_vnid(resource_id, related_resource_type, 'large')
    elif resource_type == 'character':
        related_data = search_resources_by_charid(resource_id, related_resource_type, 'large')
    else:
        raise ValueError(f"Invalid resource_type: {resource_type}. Only 'vn' and 'character' are supported.")

    if not related_data or not isinstance(related_data, dict) or not related_data.get('results'):
        raise ValueError(f"No related {related_resource_type} found for {resource_type} {resource_id}")

    update_results = {}

    for item in related_data['results']:
        id = item['id']
        try:
            update_data = convert_remote_to_local(related_resource_type, item) 
            if exists(related_resource_type, id):
                data = update(related_resource_type, id, update_data)
            else:
                data = create(related_resource_type, id, update_data)
            if not data:
                update_results[id] = False
            else:
                update_results[id] = True
            
        except Exception as exc:
            update_results[id] = False

    return {
        'status': 'SUCCESS' if update_results else 'NOT_FOUND',
        'result': update_results
    }

@error_handler
def _delete_related_resources_task(resource_type: str, resource_id: str, related_resource_type: str) -> Dict[str, Any]:
    deleted_count = delete_all_related(resource_type, resource_id, related_resource_type)
    return {
        'status': 'SUCCESS' if deleted_count else 'NOT_FOUND',
        'result': deleted_count
    }

@celery.task
def get_related_characters_images_task(*args, **kwargs) -> Dict[str, Any]:
    return _get_related_characters_images_task(*args, **kwargs)

@celery.task
def update_related_characters_images_task(*args, **kwargs) -> Dict[str, Any]:
    return _update_related_characters_images_task(*args, **kwargs)

@celery.task
def delete_related_characters_images_task(*args, **kwargs) -> Dict[str, Any]:
    return _delete_related_characters_images_task(*args, **kwargs)

@celery.task
def get_related_resources_task(*args, **kwargs) -> Dict[str, Any]:
    return _get_related_resources_task(*args, **kwargs)

@celery.task
def search_related_resources_task(*args, **kwargs) -> Dict[str, Any]:
    return _search_related_resources_task(*args, **kwargs)

@celery.task
def update_related_resources_task(*args, **kwargs) -> Dict[str, Any]:
    return _update_related_resources_task(*args, **kwargs)

@celery.task
def delete_related_resources_task(*args, **kwargs) -> Dict[str, Any]:
    return _delete_related_resources_task(*args, **kwargs)