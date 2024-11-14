from flask import Blueprint, render_template
from .search_test import search_test_routes
from .crud_test import crud_test_routes
from .data_test import data_test_routes
from .update_test import update_test_routes
from .delete_test import delete_test_routes
from .cleanup_test import cleanup_test_routes
from .backup_restore_test import backup_restore_test_routes

test_bp = Blueprint('test', __name__, url_prefix='/test')

test_bp.register_blueprint(search_test_routes)
test_bp.register_blueprint(crud_test_routes)
test_bp.register_blueprint(data_test_routes)
test_bp.register_blueprint(update_test_routes)
test_bp.register_blueprint(delete_test_routes)
test_bp.register_blueprint(cleanup_test_routes)
test_bp.register_blueprint(backup_restore_test_routes)

@test_bp.route('/')
def index():
    return render_template('test_index.html')