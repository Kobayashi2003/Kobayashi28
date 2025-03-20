from vndb import create_app as vndb_create_app
from imgserve import create_app as imgserve_create_app

vndb_app = vndb_create_app()
imgserve_app = imgserve_create_app()

vndb_celery = vndb_app.celery
imgserve_celery = imgserve_app.celery
