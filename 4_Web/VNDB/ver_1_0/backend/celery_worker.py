import vndb
import imgserve

vndb_app = vndb.create_app()
vndb_config = vndb_app.config
vndb_celery = vndb_app.celery

imgserve_app = imgserve.create_app()
imgserve_config = imgserve_app.config
imgserve_celery = imgserve_app.celery