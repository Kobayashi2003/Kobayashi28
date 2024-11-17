from api import celery
from api.search import search_local
from api.search import search_remote

@celery.task(bind=True)
def search_task(self, search_from, search_type, response_size, params,
                page = None, limit = None, sort = 'id', order = 'asc'):
    self.update_state(state='PROGRESS', meta={'status': f'Searching {search_from} database...'})
    
    try:
        if search_from == 'local':
            search_results = search_local(search_type, params, response_size,
                                          page, limit, sort, order)
        elif search_from == 'remote':
            search_results = search_remote(search_type, params, response_size,
                                           page, limit, sort, order)
        else:
            raise ValueError(f"Invalid search_from value: {search_from}")

        return {
            'status': 'SUCCESS',
            'result': search_results
        }

    except Exception as e:
        self.update_state(state='FAILURE', meta={'status': f'Search failed: {str(e)}'})
        raise