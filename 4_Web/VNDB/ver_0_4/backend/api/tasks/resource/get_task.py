from typing import Optional, Dict, Any

from api import celery
from api.database import get, get_all, exists
from api.utils import convert_model_to_dict

@celery.task(bind=True)
def get_resources_task(self, resource_type: str, id: Optional[str] = None, page: Optional[int] = None, limit: Optional[int] = None, sort: Optional[str] = None, order: str = 'asc'):
    if id:
        return get_single_resource(self, resource_type, id)
    else:
        return get_all_resources(self, resource_type, page, limit, sort, order)

def get_single_resource(self, resource_type: str, id: str) -> Dict[str, Any]:
    self.update_state(state='PROGRESS', meta={'status': f'Fetching {resource_type} with id {id}...'})

    try:
        local_type = f'local_{resource_type}'
        if not exists(local_type, id):
            return {'status': 'NOT_FOUND', 'result': None}

        result = get(resource_type, id)
        if not result:
            return {'status': 'NOT_FOUND', 'result': None}

        return {'status': 'SUCCESS', 'result': convert_model_to_dict(result)}
    except Exception as exc:
        self.update_state(state='FAILURE', meta={'status': f'Get operation failed: {str(exc)}'})
        return {'status': 'FAILURE', 'result': str(exc)}

def get_all_resources(self, resource_type: str, page: Optional[int], limit: Optional[int], sort: Optional[str], order: str) -> Dict[str, Any]:
    self.update_state(state='PROGRESS', meta={'status': f'Fetching all {resource_type}s...'})

    try:
        local_type = f'local_{resource_type}'
        local_ids = set(item.id for item in get_all(local_type))
        if not local_ids:
            return {'status': 'NOT_FOUND', 'result': None}

        result = get_all(resource_type, page=page, limit=limit, sort=sort, order=order)
        filtered_result = [item for item in result if item.id in local_ids]

        if not filtered_result:
            return {'status': 'NOT_FOUND', 'result': None}

        return {'status': 'SUCCESS', 'result': convert_model_to_dict(filtered_result)}
    except Exception as exc:
        self.update_state(state='FAILURE', meta={'status': f'Get operation failed: {str(exc)}'})
        return {'status': 'FAILURE', 'result': str(exc)}