from typing import Optional, Dict, Any, List
from sqlalchemy.exc import SQLAlchemyError
from celery import Task

from api import celery
from api.database import create, update, exists, get_all
from api.search import search_remote, search_resources_by_vnid, search_resources_by_charid
from api.utils import convert_remote_to_local

@celery.task(bind=True)
def update_related_resources_task(
    self: Task,
    resource_type: str,
    resource_id: str,
    related_resource_type: str
) -> Dict[str, Any]:
    """
    Celery task to update related resources.

    Args:
        self (Task): The Celery task instance.
        resource_type (str): The type of the main resource ('vn' or 'character').
        resource_id (str): The ID of the main resource.
        related_resource_type (str): The type of the related resources to update.

    Returns:
        Dict[str, Any]: A dictionary containing the status and result of the update operation.
    """
    self.update_state(state='PROGRESS', meta={'status': f'Updating related {related_resource_type} for {resource_type} {resource_id}...'})

    try:
        # Get related resource data
        if resource_type == 'vn':
            related_data = search_resources_by_vnid(resource_id, related_resource_type, 'large')
        elif resource_type == 'character':
            related_data = search_resources_by_charid(resource_id, related_resource_type, 'large')
        else:
            return {'status': 'FAILURE', 'result': f"Invalid resource_type: {resource_type}. Only 'vn' and 'character' are supported."}

        if not related_data or not isinstance(related_data, dict) or not related_data.get('results'):
            return {'status': 'NOT_FOUND', 'result': f"No related {related_resource_type} found for {resource_type} {resource_id}"}

        updated_count = 0
        failed_count = 0

        for item in related_data['results']:
            try:
                if 'id' not in item:
                    raise ValueError(f"Missing 'id' in resource data")

                id = item['id']
                update_data = convert_remote_to_local(related_resource_type, item)

                if exists(related_resource_type, id):
                    update(related_resource_type, id, update_data)
                else:
                    create(related_resource_type, id, update_data)

                updated_count += 1
                self.update_state(state='PROGRESS', meta={'status': f'Updated {updated_count} resources, {failed_count} failed'})

            except (ValueError, SQLAlchemyError) as exc:
                failed_count += 1
                self.update_state(state='PROGRESS', meta={'status': f'Updated {updated_count} resources, {failed_count} failed. Last error: {str(exc)}'})

        return {
            'status': 'SUCCESS',
            'result': f'Updated {updated_count} related {related_resource_type}, {failed_count} failed'
        }

    except Exception as exc:
        self.update_state(state='FAILURE', meta={'status': f'Update of related resources failed: {str(exc)}'})
        return {'status': 'FAILURE', 'result': str(exc)}

@celery.task(bind=True)
def update_resources_task(self: Task, resource_type: str, id: Optional[str] = None) -> Dict[str, Any]:
    """
    Celery task to update resources either individually or in bulk.

    Args:
        self (Task): The Celery task instance.
        resource_type (str): The type of resource to update.
        id (Optional[str]): The ID of the specific resource to update, if any.

    Returns:
        Dict[str, Any]: A dictionary containing the status and result of the update operation.
    """
    if id:
        return update_single_resource(self, resource_type, id)
    else:
        return update_all_resources(self, resource_type)

def update_single_resource(self: Task, resource_type: str, id: str) -> Dict[str, Any]:
    """
    Update a single resource in the local database based on remote data.

    Args:
        self (Task): The Celery task instance.
        resource_type (str): The type of resource to update.
        id (str): The ID of the resource to update.

    Returns:
        Dict[str, Any]: A dictionary containing the status and result of the update operation.
    """
    self.update_state(state='PROGRESS', meta={'status': 'Searching remote database...'})
    remote_result = search_remote(resource_type, {'id': id}, 'large')
    
    if not remote_result or not remote_result.get('results'): 
        return {'status': 'NOT_FOUND', 'result': None}

    update_data = convert_remote_to_local(resource_type, remote_result['results'][0])

    self.update_state(state='PROGRESS', meta={'status': 'Updating local database...'})

    try:
        # Update or create in main database
        if exists(resource_type, id):
            update(resource_type, id, update_data)
        else:
            create(resource_type, id, update_data)

        return {'status': 'SUCCESS', 'result': update_data}

    except Exception as exc:
        self.update_state(state='FAILURE', meta={'status': f'Update operation failed: {str(exc)}'})
        return {'status': 'FAILURE', 'result': str(exc)}

def update_all_resources(self: Task, resource_type: str) -> Dict[str, Any]:
    """
    Update all resources of a given type in the local database based on remote data.

    Args:
        self (Task): The Celery task instance.
        resource_type (str): The type of resources to update.

    Returns:
        Dict[str, Any]: A dictionary containing the status and result of the bulk update operation.
    """
    self.update_state(state='PROGRESS', meta={'status': 'Fetching all resources...'})
    
    try:
        resources: List[Any] = get_all(resource_type)
        
        updated_count = 0
        failed_count = 0
        
        for resource in resources:
            result = update_single_resource(self, resource_type, resource.id)
            if result['status'] == 'SUCCESS':
                updated_count += 1
            else:
                failed_count += 1
            
            # Update the task state with the current progress
            self.update_state(state='PROGRESS', meta={'status': f'Updated {updated_count} resources, {failed_count} failed'})

        return {
            'status': 'SUCCESS',
            'result': f'Updated {updated_count} resources, {failed_count} failed'
        }

    except Exception as exc:
        self.update_state(state='FAILURE', meta={'status': f'Bulk update operation failed: {str(exc)}'})
        return {'status': 'FAILURE', 'result': str(exc)}