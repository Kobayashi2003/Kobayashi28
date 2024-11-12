from datetime import datetime

from api import celery
from ..database import create, update, exists
from ..search import search_remote
from ..utils import convert_remote_to_local

@celery.task(bind=True)
def update_data_task(self, update_type, id):
    self.update_state(state='PROGRESS', meta={'status': 'Searching remote database...'})
    remote_result = search_remote(update_type, {'id': id}, 'large')
    
    if not remote_result or not remote_result['results']: 
        return {'status': 'NOT_FOUND', 'result': None}

    update_data = convert_remote_to_local(update_type, remote_result['results'][0])

    self.update_state(state='PROGRESS', meta={'status': 'Updating local database...'})

    try:
        if exists(update_type, id):
            update(update_type, id, update_data)
        else:
            create(update_type, id, update_data)

        local_type = f'local_{update_type}'
        if exists(local_type, id):
            update(local_type, id, {'last_updated': datetime.now()})
        else:
            create(local_type, id, {'last_updated': datetime.now()})

        return {'status': 'SUCCESS', 'result': update_data}

    except Exception as e:
        self.update_state(state='FAILURE', meta={'status': f'Update operation failed: {str(e)}'})
        raise