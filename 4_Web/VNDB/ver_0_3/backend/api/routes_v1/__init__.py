from flask import Blueprint

api_bp = Blueprint('api_v1', __name__, url_prefix='/api/v1')

from .hello import hello_bp

api_bp.register_blueprint(hello_bp)

from .backup_restore import backup_restore_bp
from .cleanup import cleanup_bp
from .crud import crud_bp
from .data import data_bp
from .delete import delete_bp
from .search import search_bp
from .update import update_bp

api_bp.register_blueprint(backup_restore_bp)
api_bp.register_blueprint(cleanup_bp)
api_bp.register_blueprint(crud_bp)
api_bp.register_blueprint(data_bp)
api_bp.register_blueprint(delete_bp)
api_bp.register_blueprint(search_bp)
api_bp.register_blueprint(update_bp)

from .test import test_bp
api_bp.register_blueprint(test_bp)
