from typing import Dict, Any, List, Union 

from api import celery
from api.database import update 

@celery.task(bind=True)
def edit_resources_task(self, resource_type: str, updates: Union[Dict[str, Any], List[Dict[str, Any]]]):
    if isinstance(updates, dict):
        updates = [updates]  # Convert single update to list
    
    self.update_state(state='PROGRESS', meta={'status': 'Starting edit operation...'})
    
    results = []
    success_count = 0
    failure_count = 0

    for i, update_data in enumerate(updates):
        if 'id' not in update_data:
            results.append({'id': None, 'status': 'FAILURE', 'result': 'No id provided for update'})
            failure_count += 1
            continue

        id = update_data.pop('id')
        result = perform_edit(self, resource_type, id, update_data)
        results.append({'id': id, **result})

        if result['status'] == 'SUCCESS':
            success_count += 1
        else:
            failure_count += 1

        self.update_state(state='PROGRESS', meta={
            'status': f'Processed {i+1}/{len(updates)} resources. '
                      f'Success: {success_count}, Failure: {failure_count}'
        })

    return {
        'status': 'COMPLETE',
        'result': {
            'total': len(updates),
            'success': success_count,
            'failure': failure_count,
            'details': results
        }
    }

def perform_edit(self, resource_type: str, id: str, update_data: Dict[str, Any]):
    self.update_state(state='PROGRESS', meta={'status': f'Editing {resource_type} with id {id}...'})

    try:
        result = update(resource_type, id, update_data)
        if result is None:
            return {'status': 'FAILURE', 'result': f'{resource_type.capitalize()} with id {id} FAILED to update'}

        return {'status': 'SUCCESS', 'result': f'{resource_type.capitalize()} with id {id} updated successfully'}

    except Exception as exc:
        return {'status': 'FAILURE', 'result': str(exc)}