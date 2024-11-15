def convert_img_to_jpg(file):
    """Convert image to JPG format using PTL."""
    import io
    from PIL import Image

    img = Image.open(file)
    if img.format != 'JPEG':
        img = img.convert('RGB')
        img_byte_arr = io.BytesIO()
        

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
    import os

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
    import os
    from flask import current_app

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

    import re
    import os
    from urllib.parse import urlparse

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

def convert_model_to_dict(model):
    from sqlalchemy.inspection import inspect
    from datetime import datetime, date
    from ..database import models

    if model is None:
        return None
    if isinstance(model, list):
        return [convert_model_to_dict(item) for item in model]
    
    result = {}
    for column in inspect(model).mapper.column_attrs:
        value = getattr(model, column.key)
        if isinstance(value, (datetime, date)):
            value = value.isoformat()
        result[column.key] = value
    
    # Handle relationships
    if isinstance(model, models.VN):
        result['local_vn'] = convert_model_to_dict(model.local_vn)
    elif isinstance(model, models.Tag):
        result['local_tag'] = convert_model_to_dict(model.local_tag)
    elif isinstance(model, models.Producer):
        result['local_producer'] = convert_model_to_dict(model.local_producer)
    elif isinstance(model, models.Staff):
        result['local_staff'] = convert_model_to_dict(model.local_staff)
    elif isinstance(model, models.Character):
        result['local_character'] = convert_model_to_dict(model.local_character)
    elif isinstance(model, models.Trait):
        result['local_trait'] = convert_model_to_dict(model.local_trait)
    
    return result

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
    
    return local_data

def convert_character(remote_data): return remote_data

def convert_producer(remote_data): return remote_data

def convert_staff(remote_data): return remote_data

def convert_tag(remote_data): return remote_data

def convert_trait(remote_data): return remote_data