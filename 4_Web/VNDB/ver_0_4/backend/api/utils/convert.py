from typing import Tuple, Union

import os
import io
import re
from PIL import Image
from urllib.parse import urlparse

from flask import current_app

def convert_id_to_savedata_path(savedata_id: str) -> str | None:
    """
    Convert a savedata ID to a file path.

    Args:
        savedata_id (str): The ID of the savedata file.

    Returns:
        str: The file path of the savedata, or None if the file doesn't exist.

    Example:
        >>> convert_id_to_savedata_path('abc123')
        '/path/to/savedatas/abc123'
    """
    savedata_folder = current_app.config['SAVEDATA_FOLDER']
    savedata_path = os.path.join(savedata_folder, savedata_id)
    return savedata_path if os.path.exists(savedata_path) else None

def convert_url_to_savedata_path(savedata_url: str) -> str | None:
    """
    Convert a savedata URL to a file path.

    Args:
        savedata_url (str): The URL of the savedata file.

    Returns:
        str: The file path of the savedata, or None if the input URL is invalid.

    Example:
        >>> convert_url_to_savedata_path('http://example.com/savedata/abc123')
        '/path/to/savedatas/abc123'
    """
    parsed_url = urlparse(savedata_url)
    savedata_id = os.path.basename(parsed_url.path)
    savedata_folder = current_app.config['SAVEDATA_FOLDER']
    savedata_path = os.path.join(savedata_folder, savedata_id)
    return savedata_path if os.path.exists(savedata_path) else None

def convert_img_to_jpg(file) -> Tuple[bool, Union[io.BytesIO, str]]:
    """
    Convert image to JPG format using PIL and validate the file.

    Args:
        file: The input file object or bytes-like object.

    Returns:
        A tuple (success, result), where:
        - success (bool): True if conversion was successful, False otherwise.
        - result (Union[io.BytesIO, str]): 
            If successful, a BytesIO object containing the JPEG image.
            If failed, a string describing the error.
    """

    try:
        # Attempt to open the file as an image
        img = Image.open(file)
        
        # Verify it's a valid image by accessing its format
        img.verify()
        
        # Reopen the image as verify() closes the file
        img = Image.open(file)
        
        if img.format != 'JPEG':
            img = img.convert('RGB')
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='JPEG')
            img_byte_arr.seek(0)
            return True, img_byte_arr
        else:
            # If it's already a JPEG, just return the original file
            file.seek(0)
            return True, file
    except IOError:
        return False, "Error: Unable to open image file. The file may be corrupted or not an image."
    except SyntaxError:
        return False, "Error: Unable to parse image file. The file may not be a valid image."
    except Exception as e:
        return False, f"Error: An unexpected error occurred: {str(e)}"
        
def convert_imgpath_to_imgid(img_path: str) -> str:
    """
    Convert an image file path to its ID.

    Args:
        img_path (str): The file path of the image.

    Returns:
        str: The ID of the image, or None if the input path is None.

    Example:
        >>> convert_imgpath_to_imgid('/path/to/images/vn/abc123.jpg')
        'abc123'
    """

    if img_path is None:
        return None

    return os.path.splitext(os.path.basename(img_path))[0]

def convert_imgurl_to_imgpath(type: str, img_url: str) -> str | None:
    """
    Convert an image URL to a file path.

    Args:
        type (str): The type of image ('vn' or 'character').
        img_url (str): The URL of the image.

    Returns:
        str: The file path of the image, or None if the input URL is None or invalid.

    Example:
        >>> convert_imgurl_to_imgpath('vn', 'http://example.com/image/vn/abc123')
        '/path/to/images/vn/abc123.jpg'
    """
    return convert_imgid_to_imgpath(type, convert_imgurl_to_imgid(img_url))

def convert_imgid_to_imgpath(type: str, img_id: str) -> str | None:
    """
    Convert an image ID to a file path.

    Args:
        type (str): The type of image ('vn' or 'character').
        img_id (str): The ID of the image.

    Returns:
        str: The file path of the image, or None if the input is invalid.

    Example:
        >>> convert_imgid_to_imgpath('vn', 'abc123')
        '/path/to/images/vn/abc123.jpg'
    """

    if type not in ['vn', 'character']:
        return None

    image_folder = current_app.config[f'IMAGE_{type.upper()}_FOLDER']
    image_path = os.path.join(image_folder, f"{img_id}.jpg")
    return image_path if os.path.exists(image_path) else None

def convert_imgurl_to_imgid(url: str) -> str:
    """
    Convert a VNDB image URL to a unique image ID.
    Works for both VN and character images.
    
    Args:
        url (str): The image URL from VNDB.
    
    Returns:
        str: A unique image ID.
    """
    parsed_url = urlparse(url)
    path = parsed_url.path
    
    # Pattern for VN images (cv, sf) and character images (ch)
    pattern = r'/(cv|sf|ch)(\.t)?/(\d+)/(\d+)\.jpg'
    
    match = re.search(pattern, path)
    if match:
        img_type, is_thumbnail, folder, img_id = match.groups()
        thumbnail_suffix = "_t" if is_thumbnail else ""
        return f"{img_type}{thumbnail_suffix}_{folder}_{img_id}"
    
    # If the pattern doesn't match, fall back to the original filename
    return re.sub(r'[^\w\-_\.]', '_', os.path.splitext(os.path.basename(path))[0])


def convert_remote_to_local(entity_type, remote_data):
    """
    Convert remote data to local database format.
    
    :param entity_type: String representing the type of entity (e.g., 'vn', 'character', etc.)
    :param remote_data: Dictionary containing the remote data
    :return: Dictionary with converted data ready for local database insertion
    """
    converters = {
        'vn': convert_vn,
        'character': convert_character,
        'producer': convert_producer,
        'staff': convert_staff,
        'tag': convert_tag,
        'trait': convert_trait
    }

    converter = converters.get(entity_type.lower())
    if not converter:
        raise ValueError(f"Unknown entity type: {entity_type}")

    remote_data.pop('id')
    
    return converter(remote_data)

def convert_vn(remote_data):
    local_data = remote_data.copy()
    
    # Convert devstatus
    devstatus_map = {0: 'Finished', 1: 'In development', 2: 'Cancelled'}
    local_data['devstatus'] = devstatus_map.get(remote_data.get('devstatus'), 'Finished')
    local_data.pop('relation', None)
    local_data.pop('relation_official', None)
    local_data.pop('role', None)
    local_data.pop('spoiler', None)
    
    return local_data

def convert_character(remote_data): 
    local_data = remote_data.copy()
    local_data.pop('role', None)
    local_data.pop('spoiler', None)
    return local_data 

def convert_producer(remote_data): return remote_data

def convert_staff(remote_data): 
    local_data = remote_data.copy()
    local_data.pop('eid', None)
    local_data.pop('role', None)
    return local_data

def convert_tag(remote_data): 
    local_data = remote_data.copy()
    local_data.pop('rating', None)
    local_data.pop('spoiler', None)
    local_data.pop('lie', None)
    return local_data

def convert_trait(remote_data):
    local_data = remote_data.copy()
    local_data.pop('spoiler', None)
    local_data.pop('lie', None)
    return local_data