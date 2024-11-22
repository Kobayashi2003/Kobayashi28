from typing import List, Dict, Union

from datetime import date, datetime

from sqlalchemy import inspect
from sqlalchemy.dialects.postgresql import JSON, JSONB, ARRAY

from .resources import VN, Character

def convert_model_to_dict(model):
    result = {}
    for column in inspect(model).mapper.column_attrs:
        value = getattr(model, column.key)
        if isinstance(value, (str, int, float, bool, type(None))):
            result[column.key] = value
        elif isinstance(value, (datetime, date)):
            result[column.key] = value.isoformat()
        elif isinstance(column.columns[0].type, ARRAY):
            if value is not None:
                result[column.key] = [
                    item if isinstance(item, (str, int, float, bool, type(None)))
                    else str(item)
                    for item in value
                ]
            else:
                result[column.key] = None
        elif isinstance(column.columns[0].type, (JSON, JSONB)):
            result[column.key] = value  # JSON and JSONB types are already serializable
        else:
            # For any other types, convert to string
            result[column.key] = str(value)
    return result

def extract_images(type: str, data: Union[VN, Character]) -> List[Dict[str, str]]:
    """
    Extract image URLs and their types from VN or Character data.
    
    Args:
        type (str): The type of data ('vn' or 'character').
        data (Union[VN, Character]): The VN or Character object to extract images from.
    
    Returns:
        List[Dict[str, str]]: A list of dictionaries, each containing a URL and its image type.
    
    Raises:
        ValueError: If an invalid type is provided.
    """
    if type == 'vn':
        urls_info = extract_images_vn(data)
    elif type == 'character':
        urls_info = extract_images_character(data)
    else:
        raise ValueError(f"Invalid type: {type}. Expected 'vn' or 'character'.")
    
    return urls_info

def extract_images_vn(vn: VN) -> List[Dict[str, str]]:
    """
    Extract image URLs and their types from a VN object.
    
    Args:
        vn (VN): The VN object to extract images from.
    
    Returns:
        List[Dict[str, str]]: A list of dictionaries, each containing a URL and its image type.
    """
    urls_info = []

    if vn.image:
        if 'url' in vn.image:
            urls_info.append({vn.image['url']: 'cv'})
        if 'thumbnail' in vn.image:
            urls_info.append({vn.image['thumbnail']: 'cv.t'})

    if vn.screenshots:
        for screenshot in vn.screenshots:
            if 'url' in screenshot:
                urls_info.append({screenshot['url']: 'sf'})
            if 'thumbnail' in screenshot:
                urls_info.append({screenshot['thumbnail']: 'sf.t'})
    
    return urls_info

def extract_images_character(character: Character) -> List[Dict[str, str]]:
    """
    Extract image URL and its type from a Character object.
    
    Args:
        character (Character): The Character object to extract image from.
    
    Returns:
        List[Dict[str, str]]: A list containing a dictionary with the URL and its image type, or an empty list if no image is found.
    """
    if character.image and 'url' in character.image:
        return [{character.image['url']: 'ch'}]
    
    return []