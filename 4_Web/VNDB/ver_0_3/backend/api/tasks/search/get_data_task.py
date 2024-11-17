from api import celery
from api.search import search_local
from api.search import search_remote

@celery.task(bind=True)
def get_data_task(self, data_type, id, data_size):
    self.update_state(state='PROGRESS', meta={'status': 'Searching local database...'})

    local_result = search_local(data_type, {'id': id}, data_size)

    if local_result:
        return {'status': 'SUCCESS', 'result': local_result['results'][0], 'source': 'local'}

    self.update_state(state='PROGRESS', meta={'status': 'Searching remote database...'})

    remote_result = search_remote(data_type, {'id': id}, data_size)

    if remote_result:
        return {'status': 'SUCCESS', 'result': remote_result['results'][0], 'source': 'remote'}

    return {'status': 'NOT_FOUND', 'result': None}