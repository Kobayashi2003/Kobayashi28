from flask import request
from flask_restx import Resource, Namespace
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.comment_service import (
    get_comment_by_id, get_all_comments, get_comments_by_user,
    get_comments_by_image, create_comment, update_comment,
    delete_comment
)
from app.schemas.comment_schemas import (
    comment_model, comment_create_model, 
    comment_update_model, paginated_comments
)
from app.utils.route_utils import (
    user_exists, image_exists,
    comment_exists, error_handler 
)
from .pagination import pagination_parser, search_pagination_parser

from .user_routes import ns as user_ns
from .image_routes import ns as image_ns

ns = Namespace('comments', description='Comment operations')

