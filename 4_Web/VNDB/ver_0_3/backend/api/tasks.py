from api.celery_app import celery
from api.search.local.search import search as search_local
from api.search.remote.search import search as search_remote
from api.search.remote.common import get_remote_filters 
from api.db.crud import create, update, delete, get, get_all, exists
from api.update.utils import convert_remote_to_local
from api.utils.logger import search_logger, crud_logger, data_logger, update_logger

@celery.task
def search_task(search_from, search_type, response_size, params):
    try:
        search_results = None

        if search_from == 'local':
            search_results = search_local(search_type, params, response_size)
            result_count = len(search_results)
            search_results = {
                'results': search_results,
                'count': result_count,
                'more': False  # Local search doesn't support pagination
            }
        elif search_from == 'remote':
            filters = get_remote_filters(search_type, params)
            search_results = search_remote(search_type, filters, response_size)

        if search_results:
            search_logger.info(f"Async {search_from} search for {search_type} completed. Found {search_results['count']} results.")
            return search_results
        else:
            search_logger.info(f"Async {search_from} search for {search_type} completed. No results found.")
            return None

    except Exception as e:
        search_logger.error(f"Error in async {search_from} search task for {search_type}: {str(e)}")
        raise

@celery.task
def crud_task(operation, model_type, id, data):
    try:
        result = None
        if operation == 'create':
            result = create(model_type, id, data)
            crud_logger.info(f"Created {model_type} with ID: {result.id}")
        elif operation == 'read':
            if id:
                result = get(model_type, id)
                crud_logger.info(f"Read {model_type} with ID: {id}")
            else:
                result = get_all(model_type)
                crud_logger.info(f"Read all {model_type} entries")
        elif operation == 'update':
            result = update(model_type, id, data)
            crud_logger.info(f"Updated {model_type} with ID: {id}")
        elif operation == 'delete':
            result = delete(model_type, id)
            crud_logger.info(f"Deleted {model_type} with ID: {id}")

        return {"success": True, "result": result}
    except Exception as e:
        crud_logger.error(f"Error in {operation.upper()} operation for {model_type}: {str(e)}")
        return {"success": False, "error": str(e)}

@celery.task(bind=True)
def get_data_task(self, data_type, id, data_size):
    self.update_state(state='PROGRESS', meta={'status': 'Searching local database...'})

    local_result = search_local(data_type, {'id': id}, data_size)

    if local_result:
        data_logger.info(f"Data for {data_type} with ID {id} found in local database.")
        return {'status': 'Completed', 'result': local_result[0]}

    self.update_state(state='PROGRESS', meta={'status': 'Searching remote database...'})

    remote_result = search_remote(data_type, {'id': id}, data_size)

    if remote_result:
        data_logger.info(f"Data for {data_type} with ID {id} found in remote database")
        return {'status': 'Completed', 'result': remote_result['results'][0]}

    data_logger.info(f"Data for {data_type} with ID {id} not found in local or remote database")
    return {'status': 'Not Found', 'result': None}

@celery.task(bind=True)
def update_data_task(self, update_type, id):

    self.update_state(state='PROGRESS', meta={'status': 'Searching remote database...'})
    remote_result = search_remote(update_type, {'id': id}, 'large')
    if remote_result and remote_result['results']: 
        update_data = convert_remote_to_local(update_type, remote_result['results'][0])

    self.update_state(state='PROGRESS', meta={'status': 'Checking local database...'})
    if exists(update_type, id):
        self.update_state(state='PROGRESS', meta={'status': 'Local database has data. Updating...'})
        update(update_type, id, update_data)
        update_logger.info(f"Updated {update_type} with ID: {id}")
        return {'status': 'Completed', 'result': update_data}
    
    self.update_state(state='PROGRESS', meta={'status': 'Local database has no data. Creating...'})
    create(update_type, id, update_data)
    update_logger.info(f"Created {update_type} with ID: {id}")
    return {'status': 'Completed', 'result': update_data}