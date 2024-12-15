from flask_restx import fields
from app import api
from .pagination import create_pagination_model
from .refs import user_ref_model 

comment_model = api.model('Comment', {
    'id': fields.Integer(readonly=True, description='The comment unique identifier'),
    'content': fields.String(required=True, description='The comment content'),
    'uid': fields.Integer(required=True, description='The user ID who made the comment'),
    'imgid': fields.Integer(required=True, description='The image ID the comment is associated with'),
    'parent_id': fields.Integer(description='The parent comment ID if this is a reply'),
    'reply_count': fields.Integer(description='Number of replies to this comment'),
    'user': fields.Nested(user_ref_model, description='The user who made the comment'),
    'created_at': fields.DateTime(readonly=True, description='Creation date'),
    'updated_at': fields.DateTime(readonly=True, description='Last update date'),
    'deleted_at': fields.DateTime(description='Deletion date')
})

comment_create_model = api.model('CommentCreate', {
    'content': fields.String(required=True, description='The comment content'),
    'imgid': fields.Integer(required=True, description='The image ID the comment is associated with'),
    'parent_id': fields.Integer(description='The parent comment ID if this is a reply')
})

comment_update_model = api.model('CommentUpdate', {
    'content': fields.String(required=True, description='The updated comment content')
})

paginated_comments = create_pagination_model('Comments', comment_model)