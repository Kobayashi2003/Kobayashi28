from flask_restx import fields
from app import api
from .pagination import create_pagination_model
from .refs import user_ref_model

tag_model = api.model('Tag', {
    'id': fields.Integer(readonly=True, description='The tag unique identifier'),
    'name': fields.String(required=True, description='The tag name'),
    'uid': fields.Integer(required=True, description='The user ID who created the tag'),
    'image_count': fields.Integer(description='Number of images using this tag'),
    'ignored_by_count': fields.Integer(description='Number of users ignoring this tag'),
    'user': fields.Nested(user_ref_model, description='The user who created the tag'),
    'created_at': fields.DateTime(readonly=True, description='Creation date'),
    'updated_at': fields.DateTime(readonly=True, description='Last update date'),
    'deleted_at': fields.DateTime(description='Deletion date')
})

tag_create_model = api.model('TagCreate', {
    'name': fields.String(required=True, description='The tag name'),
})

tag_update_model = api.model('TagUpdate', {
    'name': fields.String(required=True, description='The new tag name')
})

paginated_tags = create_pagination_model('Tags', tag_model)