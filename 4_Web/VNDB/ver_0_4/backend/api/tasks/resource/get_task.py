from typing import Optional, Dict, Any
from celery import Task

from api import celery
from api.database import get, get_all, get_all_related, convert_model_to_dict

@celery.task(bind=True)
def get_related_resources_task(
    self: Task,
    resource_type: str,
    resource_id: str,
    related_resource_type: str
) -> Dict[str, Any]:
    self.update_state(state='PROGRESS', meta={'status': f'Fetching related {related_resource_type}s for {resource_type} with id {resource_id}...'})

    try:
        result = get_all_related(resource_type, resource_id, related_resource_type)

        return {
            'status': 'SUCCESS' if result else 'NOT_FOUND',
            'result': result if result else None
        }
    except ValueError as exc:
        self.update_state(state='FAILURE', meta={'status': f'Invalid resource type or related resource type: {str(exc)}'})
        return {'status': 'FAILURE', 'result': str(exc)}
    except Exception as exc:
        self.update_state(state='FAILURE', meta={'status': f'Get related resources operation failed: {str(exc)}'})
        return {'status': 'FAILURE', 'result': str(exc)}

@celery.task(bind=True)
def get_resources_task(
    self: Task,
    resource_type: str,
    id: Optional[str] = None,
    page: Optional[int] = None,
    limit: Optional[int] = None,
    sort: Optional[str] = None,
    order: str = 'asc'
) -> Dict[str, Any]:
    if id:
        return get_single_resource(self, resource_type, id)
    else:
        return get_all_resources(self, resource_type, page, limit, sort, order)

def get_single_resource(self: Task, resource_type: str, id: str) -> Dict[str, Any]:
    self.update_state(state='PROGRESS', meta={'status': f'Fetching {resource_type} with id {id}...'})

    try:
        result = get(resource_type, id)
        if not result:
            return {'status': 'NOT_FOUND', 'result': None}
        
        return {'status': 'SUCCESS', 'result': convert_model_to_dict(result)}

    except Exception as exc:
        self.update_state(state='FAILURE', meta={'status': f'Get operation failed: {str(exc)}'})
        return {'status': 'FAILURE', 'result': str(exc)}

def get_all_resources(
    self: Task,
    resource_type: str,
    page: Optional[int],
    limit: Optional[int],
    sort: Optional[str],
    order: str
) -> Dict[str, Any]:
    self.update_state(state='PROGRESS', meta={'status': f'Fetching all {resource_type}s...'})

    try:
        result = get_all(resource_type, page=page, limit=limit, sort=sort, order=order)
        
        result = [convert_model_to_dict(item) for item in result]
        
        if not result:
            return {'status': 'NOT_FOUND', 'result': None}
        
        return {'status': 'SUCCESS', 'result': result}

    except Exception as exc:
        self.update_state(state='FAILURE', meta={'status': f'Get operation failed: {str(exc)}'})
        return {'status': 'FAILURE', 'result': str(exc)}