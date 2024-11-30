from typing import Dict, Any, Callable

from api.search import (
    search_resources_by_vnid_local,
    search_resources_by_charid_local,
    search_vns_by_resource_id_local,
    search_characters_by_resource_id_local,
    search_resources_by_vnid_remote, 
    search_resources_by_charid_remote,
    search_vns_by_resource_id_remote, 
    search_characters_by_resource_id_remote
)
from api.database import (
    exists, create, update, delete,
    get_images, create_image, delete_image, delete_images,
    convert_model_to_dict
)
from api.utils import (
    convert_remote_to_local, convert_imgurl_to_imgid,
    get_image_folder, download_images 
)
from .common import (
    task_with_memoize, task_with_cache_clear, format_results
) 

def unpaginated_search(search_function: Callable, **kwargs) -> Dict[str, Any]:
    results = []
    page = 1
    more = True
    while more:
        response = search_function(**kwargs, page=page)
        if response.get('status', 'FAILED') == 'SUCCESS':
            results.extend(response.get('results', []))
            more = response.get('more', False)
        else:
            more = False
        page += 1
    
    return results

@task_with_memoize(timeout=600)
def get_related_characters_images_task(vnid: str) -> Dict[str, Any]:
    results = {}

    characters = unpaginated_search(
        get_related_resources_task,
        resource_type='vn', resource_id=vnid,
        related_resource_type='character', response_size='large'    
    )
    for char in characters:
        charid = char['id']
        images = get_images('character', charid)
        results[charid] = convert_model_to_dict(images[0]) if images else None

    return format_results(results)

@task_with_cache_clear
def update_related_characters_images_task(vnid: str) -> Dict[str, Any]:
    characters = unpaginated_search(
        get_related_resources_task,
        resource_type='vn', resource_id=vnid,
        related_resource_type='character', response_size='large'    
    )

    urls_to_download = {char['image']['url']: char['id'] 
        for char in characters if char.get('image') and char['image'].get('url')}
    if not urls_to_download:
        return {"status": "NOT_FOUND", "result": None}
    
    download_folder = get_image_folder('character')
    download_results = download_images(urls_to_download.keys(), download_folder)

    successful_downloads = [url for url, success in download_results.items() if success]
    if not successful_downloads:
        raise RuntimeError("No successful downloads")

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

    return format_results(download_results)

@task_with_cache_clear
def delete_related_characters_images_task(vnid: str) -> Dict[str, Any]:
    results = {}

    characters = unpaginated_search(
        get_related_resources_task,
        resource_type='vn', resource_id=vnid,
        related_resource_type='character', response_size='large'    
    )
    for char in characters:
        charid = char['id']
        deleted_count = delete_images('character', charid)
        results[charid] = deleted_count

    return format_results(results)

@task_with_memoize(timeout=600)
def get_related_resources_task(resource_type: str, resource_id: str, related_resource_type: str, response_size: str = 'small',
                                page: int = 1, limit: int = 100, sort: str = 'id', reverse: bool = False, count: bool = True) -> Dict[str, Any]:
    if resource_type == 'vn' and related_resource_type in ['vn', 'tag', 'producer', 'staff', 'character', 'release',]:
        results = search_resources_by_vnid_local(
            vnid=resource_id, related_resource_type=related_resource_type, response_size=response_size,
            page=page, limit=limit, sort=sort, reverse=reverse, count=count
        )
    elif resource_type == 'character' and related_resource_type in ['vn', 'trait']:
        results = search_resources_by_charid_local(
            charid=resource_id, related_resource_type=related_resource_type, response_size=response_size,
            page=page, limit=limit, sort=sort, reverse=reverse, count=count
        )
    elif resource_type in ['tag', 'character', 'staff', 'producer'] and related_resource_type == 'vn':
        results = search_vns_by_resource_id_local(
            resource_type=resource_type, resource_id=resource_id, response_size=response_size,
            page=page, limit=limit, sort=sort, reverse=reverse, count=count
        )
    elif resource_type in ['vn', 'trait'] and related_resource_type == 'character':
        results = search_characters_by_resource_id_local(
            resource_type=resource_type, resource_id=resource_id, response_size=response_size, 
            page=page, limit=limit, sort=sort, reverse=reverse, count=count
        )
    else:
        raise ValueError(f"Invalid combination of resource_type and related_resource_type: {resource_type} and {related_resource_type}")
   
    if not results or not isinstance(results, dict) or not results.get('results'):
        return {'status': 'NOT_FOUND', 'result': None}

    results = format_results(results)
    results['status'] = 'SUCCESS'
    results['source'] = 'local'

    return results

@task_with_memoize(timeout=600)
def search_related_resources_task(resource_type: str, resource_id: str, related_resource_type: str, response_size: str = 'small',
                                   page: int = 1, limit: int = 100, sort: str = 'id', reverse: bool = False, count: bool = True) -> Dict[str, Any]:

    if resource_type == 'vn' and related_resource_type in ['vn', 'tag', 'producer', 'staff', 'release']:
        results = search_resources_by_vnid_remote(
            vnid=resource_id, related_resource_type=related_resource_type, response_size=response_size,
            page=page, limit=limit, sort=sort, reverse=reverse, count=count
        )
    elif resource_type == 'character' and related_resource_type in ['trait']:
        results = search_resources_by_charid_remote(
            charid=resource_id, related_resource_type=related_resource_type, response_size=response_size,
            page=page, limit=limit, sort=sort, reverse=reverse, count=count
        )
    elif resource_type in ['tag', 'dtag', 'producer', 'staff', 'character', 'release'] and related_resource_type == 'vn':
        results = search_vns_by_resource_id_remote(
            resource_type=resource_type, resource_id=resource_id, response_size=response_size,
            page=page, limit=limit, sort=sort, reverse=reverse, count=count
        )
    elif resource_type in ['trait', 'dtrait', 'vn'] and related_resource_type == 'character':
        results = search_characters_by_resource_id_remote(
            resource_type=resource_type, resource_id=resource_id, response_size=response_size, 
            page=page, limit=limit, sort=sort, reverse=reverse, count=count
        )
    else:
        raise ValueError(f"Invalid combination of resource_type and related_resource_type: {resource_type} and {related_resource_type}")
    
    if not results or not isinstance(results, dict) or not results.get('results'):
        return {'status': 'NOT_FOUND', 'result': None}

    results = format_results(results)
    results['status'] = 'SUCCESS'
    results['source'] = 'remote'

    return results

@task_with_cache_clear
def update_related_resources_task(resource_type: str, resource_id: str, related_resource_type: str) -> Dict[str, Any]:

    related_data = unpaginated_search(
        search_related_resources_task, 
        resource_type=resource_type, resource_id=resource_id, 
        related_resource_type=related_resource_type, response_size='large'
    )

    update_results = {}

    for item in related_data:
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

    return format_results(update_results)

@task_with_cache_clear
def delete_related_resources_task(resource_type: str, resource_id: str, related_resource_type: str) -> Dict[str, Any]:

    related_data = unpaginated_search(
        get_related_resources_task,
        resource_type=resource_type, resource_id=resource_id,
        related_resource_type=related_resource_type, response_size='large'    
    )

    delete_results = {}

    for item in related_data:
        id = item['id']
        try:
            data = delete(related_resource_type, id)
            if not data:
                delete_results[id] = False
            else:
                delete_results[id] = True

        except Exception as exc:
            delete_results = False

    return format_results(delete_results)