from typing import Dict, List, Any

import io
import os

from api.database import (
    get, get_image, get_images,
    create_image, create_upload_image,
    delete_image, delete_images, extract_images
)
from api.utils import (
    download_image, download_images, 
    convert_img_to_jpg, convert_imgurl_to_imgid,
    get_image_folder
)
from .common import (
    task_with_memoize, task_with_cache_clear, 
    format_results, NOT_FOUND
)

@task_with_memoize(timeout=600)
def get_image_task(resource_type: str, resource_id: str, image_id: str) -> Dict[str, Any]:
    image = get_image(resource_type, resource_id, image_id)
    return format_results(image)

@task_with_memoize(timeout=600)
def get_images_task(resource_type: str, resource_id: str) -> Dict[str, Any]:
    images = get_images(resource_type, resource_id)
    return format_results(images)

@task_with_cache_clear
def upload_image_task(resource_type: str, resource_id: str, file: Dict[str, Any]) -> Dict[str, Any]:
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

    return format_results(image)

@task_with_cache_clear
def upload_images_task(resource_type: str, resource_id: str, files: List[Dict]) -> Dict[str, Any]:
    upload_results = {}
    for file in files:
        filename = file['filename']
        if not filename:
            raise ValueError("Filename is missing")
        result = upload_image_task(resource_type, resource_id, filename, file)
        upload_results[filename] = True if result.get('status') == 'SUCESS' else False

    return format_results(upload_results)

@task_with_cache_clear
def update_image_task(resource_type: str, resource_id: str, image_id: str) -> Dict[str, Any]:
    resource_data = get(resource_type, resource_id)
    if not resource_data:
        raise ValueError(f"Resource {resource_id} not found")

    urls_info = extract_images(resource_type, resource_data)
    for url_info in urls_info:
        url, type = next(iter(url_info.items()))
        if convert_imgurl_to_imgid(url) == image_id:
            url_to_download = url
            image_type = type
            break
    else:
        return NOT_FOUND

    download_folder = get_image_folder(resource_type)
    download_result = download_image(url_to_download, download_folder)

    if not download_result:
        raise RuntimeError(f"Failed to download image {url_to_download}")

    delete_image(resource_type, resource_id, image_id)
    image = create_image(resource_type, resource_id, image_id, {"image_type": image_type})

    return format_results(image)

@task_with_cache_clear
def update_images_task(resource_type: str, resource_id: str) -> Dict[str, Any]:
    resource_data = get(resource_type, resource_id)
    if not resource_data:
        raise ValueError(f"Resource {resource_id} not found")

    urls_info = extract_images(resource_type, resource_data)
    urls_to_download = [next(iter(url_info.keys())) for url_info in urls_info]
    if not urls_to_download:
        return NOT_FOUND

    download_folder = get_image_folder(resource_type)
    download_results = download_images(urls_to_download, download_folder)

    successful_downloads = [url for url, success in download_results.items() if success]

    if not successful_downloads:
        raise RuntimeError("Failed to download any image")

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

    return format_results(download_results)

@task_with_cache_clear
def delete_image_task(resource_type: str, resource_id: str, image_id: str) -> Dict[str, Any]:
    result = delete_image(resource_type, resource_id, image_id)
    return format_results(result)

@task_with_cache_clear
def delete_images_task(resource_type: str, resource_id: str) -> Dict[str, Any]:
    deleted_count = delete_images(resource_type, resource_id)
    return format_results(deleted_count) 