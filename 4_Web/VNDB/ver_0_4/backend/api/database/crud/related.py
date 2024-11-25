from typing import List, Dict, Any

from .common import db_transaction
from .base import _get, _delete
from ..models import MODEL_MAP, convert_model_to_dict

@db_transaction
def get_all_related(resource_type: str, resource_id: str, related_resource_type: str) -> List[Dict[str, Any]]:
    resource = _get(resource_type, resource_id)
    if not resource:
        return []

    if resource_type == 'vn':
        related_field = {
            'vn': 'relations',
            'tag': 'tags',
            'character': 'characters',
            'producer': 'developers',
            'staff': 'staff'
        }.get(related_resource_type)
        related_model = MODEL_MAP[related_resource_type]
    elif resource_type == 'character':
        related_field = {
            'vn': 'vns',
            'trait': 'traits'
        }.get(related_resource_type)
        related_model = MODEL_MAP[related_resource_type]
    else:
        raise ValueError(f"Invalid resource_type: {resource_type}")

    if not related_field or not related_model:
        raise ValueError(f"Invalid related_resource_type: {related_resource_type} for resource_type: {resource_type}")
    
    related_items = getattr(resource, related_field, [])
    for item in related_items:
        local_item = _get(related_resource_type, item['id'])
        if local_item:
            item.update(convert_model_to_dict(local_item))
            item['is_exists'] = True
        else:
            item['is_exists'] = False

    return related_items

@db_transaction
def delete_all_related(resource_type: str, resource_id: str, related_resource_type: str) -> int:
    resource = _get(resource_type, resource_id)
    if not resource:
        return 0

    if resource_type == 'vn':
        related_field = {
            'vn': 'relations',
            'tag': 'tags',
            'character': 'characters',
            'producer': 'developers',
            'staff': 'staff'
        }.get(related_resource_type)
        related_model = MODEL_MAP[related_resource_type]
    elif resource_type == 'character':
        related_field = {
            'vn': 'vns',
            'trait': 'traits'
        }.get(related_resource_type)
        related_model = MODEL_MAP[related_resource_type]
    else:
        raise ValueError(f"Invalid resource_type: {resource_type}")

    if not related_field or not related_model:
        raise ValueError(f"Invalid related_resource_type: {related_resource_type} for resource_type: {resource_type}")

    related_items = getattr(resource, related_field, [])
    deleted_count = 0

    for item in related_items:
        if 'id' in item:
            deleted_item = _delete(related_resource_type, item['id'])
            if deleted_item:
                deleted_count += 1

    return deleted_count