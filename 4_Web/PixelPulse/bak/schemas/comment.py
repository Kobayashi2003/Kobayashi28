from flask_restx import fields
from app import api
from .common import timestamp_fields, create_pagination_model, user_ref_model

# Comment model
comment_model = api.model('Comment', {
    'id': fields.Integer(readonly=True, description='The comment unique identifier'),
    'content': fields.String(required=True, description='The comment content'),
    'uid': fields.Integer(required=True, description='The user ID who made the comment'),
    'imgid': fields.Integer(required=True, description='The image ID the comment is associated with'),
    'parent_id': fields.Integer(description='The parent comment ID if this is a reply'),
    'reply_count': fields.Integer(description='Number of replies to this comment'),
    'user': fields.Nested(user_ref_model, description='The user who made the comment'),
    **timestamp_fields
})

# Comment creation model
comment_create_model = api.model('CommentCreate', {
    'content': fields.String(required=True, description='The comment content'),
    'user_id': fields.Integer(required=True, description='The user ID making the comment'),
    'image_id': fields.Integer(required=True, description='The image ID the comment is associated with'),
    'parent_id': fields.Integer(description='The parent comment ID if this is a reply')
})

# Comment update model
comment_update_model = api.model('CommentUpdate', {
    'content': fields.String(required=True, description='The updated comment content')
})

# Paginated comments model
paginated_comments = create_pagination_model('Comments', comment_model)

# Comment reference model (for when you need to reference a comment in another model)
comment_ref_model = api.model('CommentReference', {
    'id': fields.Integer(readonly=True, description='The comment unique identifier'),
    'content': fields.String(description='The comment content')
})
