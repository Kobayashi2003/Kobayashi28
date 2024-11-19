from typing import Optional, Dict, Any, Union
from celery import Task

from api import celery
from api.search import search_local, search_remote

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
    """
    Celery task to search for resources either in local or remote database.

    Args:
        self (Task): The Celery task instance.
        resource_type (str): The type of resource to search for.
        search_from (str): Where to search ('local' or 'remote').
        params (Dict[str, Any]): Search parameters.
        response_size (str): Size of the response data ('small' or 'large').
        page (Optional[int]): Page number for pagination.
        limit (Optional[int]): Number of items per page.
        sort (str): Field to sort by.
        order (str): Sort order ('asc' or 'desc').

    Returns:
        Dict[str, Any]: A dictionary containing the search results and status.
    """
    self.update_state(state='PROGRESS', meta={'status': f'Searching {search_from} database for {resource_type}...'})
    
    try:
        # Perform search based on the specified database (local or remote)
        if search_from == 'local':
            search_results = search_local(resource_type, params, response_size, page, limit, sort, order)
        elif search_from == 'remote':
            search_results = search_remote(resource_type, params, response_size, page, limit, sort, order)
        else:
            return {'status': 'FAILURE', 'result': f"Invalid search_from value: {search_from}"}

        # Check if search results are valid
        if not search_results or not (isinstance(search_results, dict) or not search_results.get('results')):
            return {'status': 'NOT_FOUND', 'result': None}

        # Add status and source to the search results
        search_results['status'] = 'SUCCESS'
        search_results['source'] = search_from

        return search_results

    except Exception as exc:
        # Update task state and return failure status if an exception occurs
        self.update_state(state='FAILURE', meta={'status': f'Search operation failed: {str(exc)}'})
        return {'status': 'FAILURE', 'result': str(exc)}

@celery.task(bind=True)
def search_resource_task(self: Task, resource_type: str, id: str, data_size: str = 'small') -> Dict[str, Any]:
    """
    Celery task to search for a specific resource by ID in both local and remote databases.

    Args:
        self (Task): The Celery task instance.
        resource_type (str): The type of resource to search for.
        id (str): The ID of the resource to search for.
        data_size (str): Size of the response data ('small' or 'large').

    Returns:
        Dict[str, Any]: A dictionary containing the search results and status.
    """
    try:
        # Search in local database
        self.update_state(state='PROGRESS', meta={'status': 'Searching local database...'})
        search_results = search_local(resource_type, {'id': id}, data_size)

        if search_results and isinstance(search_results, dict) and search_results.get('results'):
            search_results['status'] = 'SUCCESS'
            search_results['source'] = 'local'
            return search_results

        # If not found in local, search in remote database
        self.update_state(state='PROGRESS', meta={'status': 'Searching remote database...'})
        search_results = search_remote(resource_type, {'id': id}, data_size)

        if search_results and isinstance(search_results, dict) and search_results.get('results'):
            search_results['status'] = 'SUCCESS'
            search_results['source'] = 'remote'
            return search_results

        # If not found in either database
        return {'status': 'NOT_FOUND', 'result': None}

    except Exception as exc:
        # Update task state and return failure status if an exception occurs
        self.update_state(state='FAILURE', meta={'status': f'Search by ID operation failed: {str(exc)}'})
        return {'status': 'FAILURE', 'result': str(exc)}