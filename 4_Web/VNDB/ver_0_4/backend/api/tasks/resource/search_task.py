from typing import Optional, Dict, Any 
from celery import Task

from api import celery
from api.search import search_local, search_remote, search_resources_by_vnid, search_resources_by_charid

@celery.task(bind=True)
def search_related_resources_task(
    self: Task,
    resource_type: str,
    resource_id: str,
    related_resource_type: str,
    response_size: str = 'small'
) -> Dict[str, Any]:
    self.update_state(state='PROGRESS', meta={'status': f'Searching for related {related_resource_type} for {resource_type} {resource_id}...'})

    try:
        search_results = None

        if resource_type == 'vn':
            search_results = search_resources_by_vnid(resource_id, related_resource_type, response_size)
        elif resource_type == 'character':
            search_results = search_resources_by_charid(resource_id, related_resource_type, response_size)
        else:
            return {'status': 'FAILURE', 'result': f"Invalid resource_type: {resource_type}. Only 'vn' and 'character' are supported."}

        if not search_results or not isinstance(search_results, dict) or not search_results.get('results'):
            return {'status': 'NOT_FOUND', 'result': None}

        search_results['status'] = 'SUCCESS'
        return search_results

    except Exception as exc:
        self.update_state(state='FAILURE', meta={'status': f'Search for related resources failed: {str(exc)}'})
        return {'status': 'FAILURE', 'result': str(exc)}

@celery.task(bind=True)
def search_resources_task(
    self: Task,
    resource_type: str,
    search_from: str,
    params: Dict[str, Any],
    response_size: str = 'small',
    page: Optional[int] = None,
    limit: Optional[int] = None,
    sort: str = 'id',
    order: str = 'asc'
) -> Dict[str, Any]:
    self.update_state(state='PROGRESS', meta={'status': f'Searching {search_from} database for {resource_type}...'})
    
    try:
        if search_from == 'local':
            search_results = search_local(resource_type, params, response_size, page, limit, sort, order)
        elif search_from == 'remote':
            search_results = search_remote(resource_type, params, response_size, page, limit, sort, order)
        else:
            return {'status': 'FAILURE', 'result': f"Invalid search_from value: {search_from}"}

        if not search_results or not (isinstance(search_results, dict) or not search_results.get('results')):
            return {'status': 'NOT_FOUND', 'result': None}

        search_results['status'] = 'SUCCESS'
        search_results['source'] = search_from

        return search_results

    except Exception as exc:
        self.update_state(state='FAILURE', meta={'status': f'Search operation failed: {str(exc)}'})
        return {'status': 'FAILURE', 'result': str(exc)}

@celery.task(bind=True)
def search_resource_task(self: Task, resource_type: str, id: str, data_size: str = 'small') -> Dict[str, Any]:
    try:
        self.update_state(state='PROGRESS', meta={'status': 'Searching local database...'})
        search_results = search_local(resource_type, {'id': id}, data_size)

        if search_results and isinstance(search_results, dict) and search_results.get('results'):
            search_results['status'] = 'SUCCESS'
            search_results['source'] = 'local'
            return search_results

        self.update_state(state='PROGRESS', meta={'status': 'Searching remote database...'})
        search_results = search_remote(resource_type, {'id': id}, data_size)

        if search_results and isinstance(search_results, dict) and search_results.get('results'):
            search_results['status'] = 'SUCCESS'
            search_results['source'] = 'remote'
            return search_results

        return {'status': 'NOT_FOUND', 'result': None}

    except Exception as exc:
        self.update_state(state='FAILURE', meta={'status': f'Search by ID operation failed: {str(exc)}'})
        return {'status': 'FAILURE', 'result': str(exc)}