from typing import List, Dict, Any, Optional

from sqlalchemy import text

from api import db
from .common import db_transaction
from .base import (
    _get, _get_all, _get_inactive, 
    _get_inactive_type, 
    _create, _delete, exists
)
from ..models import IMAGE_MODEL_MAP, ImageModelType

def next_image_id(resource_type: str) -> str:
    """
    Get the next available image ID starting with 'u' without using a database session.

    Args:
        resource_type (str): The type of resource ('vn' or 'character').

    Returns:
        str: The next available image ID.

    Raises:
        ValueError: If an invalid resource_type is provided.
    """
    table_name = IMAGE_MODEL_MAP.get(resource_type).__tablename__
    if not table_name:
        raise ValueError(f"Invalid image resource_type: {resource_type}")

    # Use raw SQL query to get the maximum ID
    query = text(f"""
        SELECT COALESCE(MAX(CAST(SUBSTRING(id, 2) AS INTEGER)), 0)
        FROM {table_name}
        WHERE id LIKE 'u%'
    """)

    with db.engine.connect() as connection:
        result = connection.execute(query)
        max_num = result.scalar()

    return f'u{max_num + 1}'

@db_transaction
def create_image(resource_type: str, resource_id: str, image_id: str, data: Dict[str, Any]) -> Optional[ImageModelType]:
    if resource_type not in ['vn', 'character']:
        raise ValueError(f"Invalid resource_type for image creation: {resource_type}")

    resource = _get(resource_type, resource_id)
    if not resource:
        return None
    
    image_type = f'{resource_type}_image'
    image_data = {
        'id': image_id,
        'image_type': data.get('image_type', 'unknown'),
        f'{resource_type}_id': resource_id
    }

    image = _create(type=image_type, id=image_id, data=image_data)
    if image is None:
        return None

    resource.images.append(image)
    return image

def create_upload_image(resource_type: str, resource_id: str, data: Dict[str, Any]) -> Optional[ImageModelType]:
    image_id = next_image_id(resource_type)
    return create_image(resource_type, resource_id, image_id, data)

@db_transaction
def get_image(resource_type: str, resource_id: str, image_id: str) -> Optional[ImageModelType]:
    if resource_type not in ['vn', 'character']:
        raise ValueError(f"Invalid resource_type for image retrieval: {resource_type}")
    
    if not exists(resource_type, resource_id):
        return None

    image = _get(f'{resource_type}_image', image_id)

    if not image or getattr(image, f'{resource_type}_id') != resource_id:
        return None
    
    return image

@db_transaction
def get_images(resource_type: str, resource_id: str) -> List[ImageModelType]:
    if resource_type not in ['vn', 'character']:
        raise ValueError(f"Invalid resource_type for image retrieval: {resource_type}")

    if not exists(resource_type, resource_id):
        return []

    images = _get_all(f'{resource_type}_image')
    return [img for img in images if getattr(img, f'{resource_type}_id') == resource_id]

@db_transaction
def delete_image(resource_type: str, resource_id: str, image_id: str) -> Optional[ImageModelType]:
    if resource_type not in ['vn', 'character']:
        raise ValueError(f"Invalid resource_type for image deletion: {resource_type}")
    
    if not exists(resource_type, resource_id):
        return None

    image_type = f'{resource_type}_image'
    image = _get(image_type, image_id) or _get_inactive(image_type, image_id)
    
    if not image or getattr(image, f'{resource_type}_id') != resource_id:
        return None
    
    return _delete(image_type, image_id)

@db_transaction
def delete_images(resource_type: str, resource_id: str) -> int:
    if resource_type not in ['vn', 'character']:
        raise ValueError(f"Invalid resource_type for image deletion: {resource_type}")
    
    if not exists(resource_type, resource_id):
        return 0

    image_type = f'{resource_type}_image'
    
    # Get all images associated with the resource
    images = _get_all(image_type) + _get_inactive_type(image_type)
    images = [img for img in images if getattr(img, f'{resource_type}_id') == resource_id]
    
    deleted_count = 0
    for image in images:
        deleted_image = _delete(image_type, image.id)
        deleted_count += 1 if deleted_image else 0
    
    return deleted_count