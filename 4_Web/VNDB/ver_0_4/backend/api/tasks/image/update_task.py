from typing import Optional, Dict, Any, Union
from celery import Task
from sqlalchemy.exc import SQLAlchemyError

import io
import os
import shutil

from api import celery
from api.database import get_image, create_image, delete_image, update, get, extract_images
from api.utils import download_images, get_image_folder, get_image_path, convert_img_to_jpg, convert_imgurl_to_imgid

@celery.task(bind=True)
def update_images_task(
    self: Task, 
    resource_type: str, 
    resource_id: str, 
    image_id: Optional[str] = None, 
    file: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Celery task to update image(s) for a given resource.

    This task can update either a single image (if image_id is provided) or all images
    associated with a specific resource. It updates its state during execution and
    returns the result of the update operation.

    Args:
        self (Task): The Celery task instance (automatically injected by Celery).
        resource_type (str): The type of resource (e.g., 'vn', 'character').
        resource_id (str): The ID of the resource.
        image_id (Optional[str]): The ID of a specific image to update, if any.
        file (Optional[Dict[str, Any]]): File data for updating a single image, if applicable.

    Returns:
        Dict[str, Any]: A dictionary containing the status and result of the update operation.
        The structure is as follows:
        {
            "status": str,  # "SUCCESS", "NOT_FOUND", or "ERROR"
            "result": Any  # Update result or error message
        }

    Raises:
        SQLAlchemyError: If there's an issue with the database operation.
        OSError: If there's an issue with file operations.
        These exceptions are handled within the task.

    Note:
        - The task updates its state to 'PROGRESS' during execution.
        - For single image update, it processes and saves the new image file.
        - For all images update, it downloads and processes all associated images.
    """

    if image_id:
        self.update_state(state='PROGRESS', meta={'status': 'Updating single image...'})
        return update_single_image(resource_type, resource_id, image_id, file)
    else:
        self.update_state(state='PROGRESS', meta={'status': 'Updating all images...'})
        return update_all_images(resource_type, resource_id)

def update_single_image(resource_type: str, resource_id: str, image_id: str, file: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update a single image for a given resource.

    Args:
        resource_type (str): The type of resource (e.g., 'vn', 'character').
        resource_id (str): The ID of the resource.
        image_id (str): The ID of the image to update.
        file (Dict[str, Any]): File data for updating the image.

    Returns:
        Dict[str, Any]: A dictionary containing the status and result of the update operation.
    """
    image_path = get_image_path(resource_type, image_id)
    image_bak_path = f"{image_path}.bak"
    
    if image_path:
        shutil.copy2(image_path, image_bak_path)

    try:
        # Check if the image exists
        image = get_image(resource_type, resource_id, image_id)
        if not image:
            return {"status": "NOT_FOUND", "result": f"Image with id {image_id} not found for {resource_type} {resource_id}"}

        # Process and save the new image
        filename = file['filename']
        file_content = io.BytesIO(file['content'])

        success, result = convert_img_to_jpg(file_content)
        if not success:
            raise ValueError(f"Failed to convert {filename} to JPG")

        with open(image_path, 'wb') as f:
            f.write(result.getvalue())
        
        # Update image metadata
        image_type = f"{resource_type}_image"
        image_data = {
            f"{resource_type}_id": resource_id,
            "image_type": "u"
        }
        update(image_type, image_id, image_data)

        # Remove backup if update was successful
        if os.path.exists(image_bak_path):
            os.remove(image_bak_path)

        return {"status": "SUCCESS", "result": f"Image {filename} updated successfully for {resource_type} {resource_id}"}

    except Exception as e:
        # Restore from backup if update failed
        if os.path.exists(image_bak_path):
            shutil.move(image_bak_path, image_path)
        elif os.path.exists(image_path):
            os.remove(image_path)
        return {"status": "ERROR", "result": str(e)}

def update_all_images(resource_type: str, resource_id: str) -> Dict[str, Any]:
    """
    Update all images for a given resource.

    Args:
        resource_type (str): The type of resource (e.g., 'vn', 'character').
        resource_id (str): The ID of the resource.

    Returns:
        Dict[str, Any]: A dictionary containing the status and result of the update operation.
    """
    try:
        # Fetch resource data and extract image URLs
        resource_data = get(resource_type, resource_id)
        if not resource_data:
            return {"status": "NOT_FOUND", "result": f"{resource_type} {resource_id} not found"}

        urls_info = extract_images(resource_type, resource_data)
        urls_to_download = [next(iter(url_info.keys())) for url_info in urls_info]
        if not urls_to_download:
            return {"status": "SUCCESS", "result": {}}

        # Download images
        download_folder = get_image_folder(resource_type)
        download_results = download_images(urls_to_download, download_folder)

        successful_downloads = [url for url, success in download_results.items() if success]
        if not successful_downloads:
            return {"status": "SUCCESS", "result": download_results}
    except Exception as e:
        return {"status": "ERROR", "result": f"Failed to download images: {str(e)}"}

    # Process downloaded images
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

    return {"status": "SUCCESS", "result": download_results}