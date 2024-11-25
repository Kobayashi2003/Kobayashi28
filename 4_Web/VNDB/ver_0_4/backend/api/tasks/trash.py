from typing import Dict, Any 

from api import celery, scheduled_task
from api.database import (
    get_inactive, get_inactive_type, _get_inactive_all,
    cleanup, cleanup_type, cleanup_all,
    recover, recover_type, recover_all,
    convert_model_to_dict
)
from .common import error_handler

@error_handler
def _cleanup_item_task(item_type: str, item_id: str) -> Dict[str, Any]:
    result = cleanup(item_type, item_id)
    return {
        'status': 'SUCCESS' if result else 'NOT_FOUND',
        'result': convert_model_to_dict(result) if result else None
    }

@error_handler
def _cleanup_type_task(item_type: str) -> Dict[str, Any]:
    result = cleanup_type(item_type)
    return {
        'status': 'SUCCESS',
        'result': result
    }

@error_handler
def _cleanup_all_task() -> Dict[str, Any]:
    result = cleanup_all()
    return {
        'status': 'SUCCESS',
        'result': result
    }

@error_handler
def _recover_item_task(item_type: str, item_id: str) -> Dict[str, Any]:
    result = recover(item_type, item_id)
    return {
        'status': 'SUCCESS' if result else 'NOT_FOUND',
        'result': convert_model_to_dict(result) if result else None
    }

@error_handler
def _recover_type_task(item_type: str) -> Dict[str, Any]:
    result = recover_type(item_type)
    return {
        'status': 'SUCCESS',
        'result': result
    }

@error_handler
def _recover_all_task() -> Dict[str, Any]:
    result = recover_all()
    return {
        'status': 'SUCCESS',
        'result': result
    }

@error_handler
def _get_inactive_item_task(item_type: str, item_id: str) -> Dict[str, Any]:
    result = get_inactive(item_type, item_id)
    return {
        'status': 'SUCCESS' if result else 'NOT_FOUND',
        'result': convert_model_to_dict(result) if result else None
    }

@error_handler
def _get_inactive_type_task(item_type: str, page: int = None, limit: int = None, sort: str = 'id', order: str = 'asc') -> Dict[str, Any]:
    result = get_inactive_type(item_type, page, limit, sort, order)
    return {
        'status': 'SUCCESS',
        'result': [convert_model_to_dict(item) for item in result]
    }

@error_handler
def _get_inactive_all_task() -> Dict[str, Any]:
    result = _get_inactive_all()
    return {
        'status': 'SUCCESS',
        'result': {k: [convert_model_to_dict(item) for item in v] for k, v in result.items()}
    }

@celery.task
def cleanup_item_task(*args, **kwargs) -> Dict[str, Any]:
    return _cleanup_item_task(*args, **kwargs)

@celery.task
def cleanup_type_task(*args, **kwargs) -> Dict[str, Any]:
    return _cleanup_type_task(*args, **kwargs)

@celery.task
def cleanup_all_task(*args, **kwargs) -> Dict[str, Any]:
    return _cleanup_all_task(*args, **kwargs)

@celery.task
def recover_item_task(*args, **kwargs) -> Dict[str, Any]:
    return _recover_item_task(*args, **kwargs)

@celery.task
def recover_type_task(*args, **kwargs) -> Dict[str, Any]:
    return _recover_type_task(*args, **kwargs)

@celery.task
def recover_all_task(*args, **kwargs) -> Dict[str, Any]:
    return _recover_all_task(*args, **kwargs)

@celery.task
def get_inactive_item_task(*args, **kwargs) -> Dict[str, Any]:
    return _get_inactive_item_task(*args, **kwargs)

@celery.task
def get_inactive_type_task(*args, **kwargs) -> Dict[str, Any]:
    return _get_inactive_type_task(*args, **kwargs)

@celery.task
def get_inactive_all_task(*args, **kwargs) -> Dict[str, Any]:
    return _get_inactive_all_task(*args, **kwargs)