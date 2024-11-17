from typing import Optional
from datetime import datetime, timezone

from api import celery
from api.database import create, update, exists, get_all
from api.search import search_remote
from api.utils import convert_remote_to_local

@celery.task(bind=True)
def update_resources_task(self, resource_type: str, id: Optional[str] = None):
    if id:
        return update_single_resource(self, resource_type, id)
    else:
        return update_all_resources(self, resource_type)

def update_single_resource(self, resource_type: str, id: str):
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

        # Update or create in local_type database
        local_type = f'local_{resource_type}'
        local_update = {'last_updated': datetime.now(timezone.utc)}
        if exists(local_type, id):
            update(local_type, id, local_update)
        else:
            create(local_type, id, local_update)

        return {'status': 'SUCCESS', 'result': update_data}

    except Exception as exc:
        self.update_state(state='FAILURE', meta={'status': f'Update operation failed: {str(exc)}'})
        return {'status': 'FAILURE', 'result': str(exc)}

def update_all_resources(self, resource_type: str):
    self.update_state(state='PROGRESS', meta={'status': 'Fetching all resources...'})
    
    try:
        local_type = f'local_{resource_type}'
        all_local_resources = get_all(local_type)
        
        updated_count = 0
        failed_count = 0
        
        for local_resource in all_local_resources:
            result = update_single_resource(self, resource_type, local_resource.id)
            if result['status'] == 'SUCCESS':
                updated_count += 1
            else:
                failed_count += 1
            
            self.update_state(state='PROGRESS', meta={
                'status': f'Updated {updated_count} resources, {failed_count} failed'
            })

        return {
            'status': 'SUCCESS',
            'result': f'Updated {updated_count} resources, {failed_count} failed'
        }

    except Exception as exc:
        self.update_state(state='FAILURE', meta={'status': f'Bulk update operation failed: {str(exc)}'})
        return {'status': 'FAILURE', 'result': str(exc)}