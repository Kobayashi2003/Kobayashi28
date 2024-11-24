from typing import Optional, Dict, Any
from celery import Task

from api import celery
from api.database import delete, delete_all, delete_all_related, convert_model_to_dict 

@celery.task(bind=True)
def delete_related_resources_task(
    self: Task,
    resource_type: str,
    resource_id: str,
    related_resource_type: str
) -> Dict[str, Any]:
    """
    Celery task to delete related resources for a given resource.

    Args:
        self (Task): The Celery task instance.
        resource_type (str): The type of the main resource ('vn' or 'character').
        resource_id (str): The ID of the main resource.
        related_resource_type (str): The type of the related resources to delete.

    Returns:
        Dict[str, Any]: A dictionary containing the status and result of the delete operation.
    """
    self.update_state(state='PROGRESS', meta={'status': f'Deleting related {related_resource_type} for {resource_type} with id {resource_id}...'})

    try:
        # Attempt to delete the related resources
        deleted_count = delete_all_related(resource_type, resource_id, related_resource_type)

        if deleted_count == 0:
            return {'status': 'NOT_FOUND', 'result': f"No related {related_resource_type} found for {resource_type} with id {resource_id}"}

        # Return success status with the number of deleted resources
        return {'status': 'SUCCESS', 'result': f"Deleted {deleted_count} related {related_resource_type} for {resource_type} with id {resource_id}"}

    except ValueError as exc:
        # Handle invalid resource types or related resource types
        self.update_state(state='FAILURE', meta={'status': f'Invalid resource type or related resource type: {str(exc)}'})
        return {'status': 'FAILURE', 'result': str(exc)}

    except Exception as exc:
        # Update task state and return failure status if an exception occurs
        self.update_state(state='FAILURE', meta={'status': f'Delete related resources operation failed: {str(exc)}'})
        return {'status': 'FAILURE', 'result': str(exc)}

@celery.task(bind=True)
def delete_resources_task(self: Task, resource_type: str, id: Optional[str] = None) -> Dict[str, Any]:
    """
    Celery task to delete resources either individually or in bulk.

    Args:
        self (Task): The Celery task instance.
        resource_type (str): The type of resource to delete.
        id (Optional[str]): The ID of the specific resource to delete, if any.

    Returns:
        Dict[str, Any]: A dictionary containing the status and result of the delete operation.
    """
    if id:
        return delete_single_resource(self, resource_type, id)
    else:
        return delete_all_resources(self, resource_type)

def delete_single_resource(self: Task, resource_type: str, id: str) -> Dict[str, Any]:
    """
    Delete a single resource from the database.

    Args:
        self (Task): The Celery task instance.
        resource_type (str): The type of resource to delete.
        id (str): The ID of the resource to delete.

    Returns:
        Dict[str, Any]: A dictionary containing the status and result of the delete operation.
    """
    self.update_state(state='PROGRESS', meta={'status': f'Deleting {resource_type} with id {id}...'})

    try:
        # Attempt to delete the resource
        result = delete(resource_type, id)
        
        if not result:
            return {'status': 'NOT_FOUND', 'result': None}

        # Convert the deleted resource to a dictionary for the response
        return {'status': 'SUCCESS', 'result': convert_model_to_dict(result)}

    except Exception as exc:
        # Update task state and return failure status if an exception occurs
        self.update_state(state='FAILURE', meta={'status': f'Delete operation failed: {str(exc)}'})
        return {'status': 'FAILURE', 'result': str(exc)}

def delete_all_resources(self: Task, resource_type: str) -> Dict[str, Any]:
    """
    Delete all resources of a given type from the database.

    Args:
        self (Task): The Celery task instance.
        resource_type (str): The type of resources to delete.

    Returns:
        Dict[str, Any]: A dictionary containing the status and result of the bulk delete operation.
    """
    self.update_state(state='PROGRESS', meta={'status': f'Deleting all {resource_type} resources...'})

    try:
        # Attempt to delete all resources of the given type
        count = delete_all(resource_type)

        if not count:
            return {'status': 'NOT_FOUND', 'result': None} 

        # Return success status with the number of deleted resources
        return {'status': 'SUCCESS', 'result': f"Deleted {count} {resource_type} resources."}

    except Exception as exc:
        # Update task state and return failure status if an exception occurs
        self.update_state(state='FAILURE', meta={'status': f'Bulk delete operation failed: {str(exc)}'})
        return {'status': 'FAILURE', 'result': str(exc)}