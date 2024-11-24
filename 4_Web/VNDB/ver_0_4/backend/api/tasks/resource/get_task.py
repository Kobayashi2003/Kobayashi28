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
    """
    Celery task to fetch related resources for a given resource.

    Args:
        self (Task): The Celery task instance.
        resource_type (str): The type of the main resource ('vn' or 'character').
        resource_id (str): The ID of the main resource.
        related_resource_type (str): The type of the related resources to retrieve.

    Returns:
        Dict[str, Any]: A dictionary containing the status and result of the fetch operation.
    """
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
    """
    Celery task to fetch resources either individually or in bulk.

    Args:
        self (Task): The Celery task instance.
        resource_type (str): The type of resource to fetch.
        id (Optional[str]): The ID of the specific resource to fetch, if any.
        page (Optional[int]): The page number for pagination.
        limit (Optional[int]): The number of items per page.
        sort (Optional[str]): The field to sort by.
        order (str): The sort order ('asc' or 'desc').

    Returns:
        Dict[str, Any]: A dictionary containing the status and result of the fetch operation.
    """
    if id:
        return get_single_resource(self, resource_type, id)
    else:
        return get_all_resources(self, resource_type, page, limit, sort, order)

def get_single_resource(self: Task, resource_type: str, id: str) -> Dict[str, Any]:
    """
    Fetch a single resource from the database.

    Args:
        self (Task): The Celery task instance.
        resource_type (str): The type of resource to fetch.
        id (str): The ID of the resource to fetch.

    Returns:
        Dict[str, Any]: A dictionary containing the status and result of the fetch operation.
    """
    self.update_state(state='PROGRESS', meta={'status': f'Fetching {resource_type} with id {id}...'})

    try:
        result = get(resource_type, id)
        if not result:
            return {'status': 'NOT_FOUND', 'result': None}
        
        # Convert the model instance to a dictionary
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
    """
    Fetch all resources of a given type from the database with optional pagination and sorting.

    Args:
        self (Task): The Celery task instance.
        resource_type (str): The type of resources to fetch.
        page (Optional[int]): The page number for pagination.
        limit (Optional[int]): The number of items per page.
        sort (Optional[str]): The field to sort by.
        order (str): The sort order ('asc' or 'desc').

    Returns:
        Dict[str, Any]: A dictionary containing the status and result of the fetch operation.
    """
    self.update_state(state='PROGRESS', meta={'status': f'Fetching all {resource_type}s...'})

    try:
        # Fetch all resources with pagination and sorting
        result = get_all(resource_type, page=page, limit=limit, sort=sort, order=order)
        
        # Convert each model instance to a dictionary
        result = [convert_model_to_dict(item) for item in result]
        
        if not result:
            return {'status': 'NOT_FOUND', 'result': None}
        
        return {'status': 'SUCCESS', 'result': result}

    except Exception as exc:
        self.update_state(state='FAILURE', meta={'status': f'Get operation failed: {str(exc)}'})
        return {'status': 'FAILURE', 'result': str(exc)}