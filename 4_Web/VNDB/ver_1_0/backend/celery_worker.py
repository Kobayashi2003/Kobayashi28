import vndb
import imgserve

vndb_app = vndb.create_app(enable_scheduler=False)
vndb_config = vndb_app.config
vndb_celery = vndb_app.celery

imgserve_app = imgserve.create_app(enable_scheduler=False)
imgserve_config = imgserve_app.config
imgserve_celery = imgserve_app.celery