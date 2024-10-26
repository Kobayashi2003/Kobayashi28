from api.celery_app import celery
from api.search.vndb import search_vndb
from api.search.local import search_local
from api.search.utils import generate_vndb_fields, generate_vndb_filters 
from api.search.utils import generate_local_fields, generate_local_filters 
from api.search.utils import VNDB_FIELDS_SIMPLE, LOCAL_FILELDS_SIMPLE
from api.download.server import download2server
from api.download.client import download2client
from api.utils.logger import download_logger, search_logger


@celery.task
def search_task(search_type, filters, fields, sort_field=None, reverse=False):
    try:
        search_results = None

        if search_type == 'local':
            local_filters = generate_local_filters(**filters)
            local_fields = generate_local_fields(fields)
            search_results = search_local(filters=local_filters, fields=local_fields, sort_field=sort_field, reverse=reverse)
        elif search_type == 'vndb':
            vndb_filters = generate_vndb_filters(**filters)
            vndb_fields = generate_vndb_fields(fields)
            search_results = search_vndb(filters=vndb_filters, fields=vndb_fields, sort_field=sort_field, reverse=reverse)

        if search_results:
            search_logger.info(f"Async combined search completed. Found {len(search_results)} results.")
            return search_results
        else:
            search_logger.info("Async combined search completed. No results found.")
            return None

    except Exception as e:
        search_logger.error(f"Error in async combined search task: {str(e)}")
        raise

@celery.task
def download_server_task(filters):
    try:
        downloaded_images = download2server(filters)
        download_logger.info(f"Async server download completed. Downloaded {len(downloaded_images)} images.")
        return downloaded_images
    except Exception as e:
        download_logger.error(f"Error in async server download task: {str(e)}")
        raise

@celery.task
def download_client_task(filters):
    try:
        zip_file_path = download2client(filters)
        download_logger.info(f"Async client download completed. Created zip file: {zip_file_path}")
        return zip_file_path
    except Exception as e:
        download_logger.error(f"Error in async client download task: {str(e)}")
        raise