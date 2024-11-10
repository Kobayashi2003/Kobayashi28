from api.celery_app import celery
from api.search.remote.search import search as search_remote
from api.search.local.search import search as search_local
from api.search.remote.common import get_remote_filters 
from api.utils.logger import search_logger, crud_logger
from api.db.crud import create, update, delete, get, get_all

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