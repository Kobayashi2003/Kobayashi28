from flask_restx import fields
from app import api
from .common import timestamp_fields, create_pagination_model, user_ref_model

# Tag model
tag_model = api.model('Tag', {
    'id': fields.Integer(readonly=True, description='The tag unique identifier'),
    'name': fields.String(required=True, description='The tag name'),
    'uid': fields.Integer(required=True, description='The user ID who created the tag'),
    'image_count': fields.Integer(description='Number of images using this tag'),
    'ignored_by_count': fields.Integer(description='Number of users ignoring this tag'),
    'user': fields.Nested(user_ref_model, description='The user who created the tag'),
    **timestamp_fields
})

# Tag creation model
tag_create_model = api.model('TagCreate', {
    'name': fields.String(required=True, description='The tag name'),
    'user_id': fields.Integer(required=True, description='The user ID creating the tag')
})

# Tag update model
tag_update_model = api.model('TagUpdate', {
    'name': fields.String(required=True, description='The new tag name')
})

# Paginated tags model
paginated_tags = create_pagination_model('Tags', tag_model)

# Popular tag model
popular_tag_model = api.model('PopularTag', {
    'tag': fields.Nested(tag_model),
    'image_count': fields.Integer(description='Number of images using this tag')
})

# Tag reference model (for when you need to reference a tag in another model)
tag_ref_model = api.model('TagReference', {
    'id': fields.Integer(readonly=True, description='The tag unique identifier'),
    'name': fields.String(description='The tag name')
})
