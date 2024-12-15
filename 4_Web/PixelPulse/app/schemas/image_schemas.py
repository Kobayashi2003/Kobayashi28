from flask_restx import fields 
from app import api
from .pagination import create_pagination_model
from .refs import user_ref_model, tag_ref_model, comment_ref_model

image_model = api.model('Image', {
    'id': fields.Integer(readonly=True, description='The image unique identifier'),
    'title': fields.String(required=True, description='The image title'),
    'description': fields.String(description='The image description'),
    'url': fields.String(required=True, description='The image url'),
    'uid': fields.Integer(required=True, description='The user ID who uploaded the image'),
    'comment_count': fields.Integer(description='Number of comments on this image'),
    'tag_count': fields.Integer(description='Number of tags on this image'),
    'collection_count': fields.Integer(description='Number of collections containing this image'),
    'liked_by_count': fields.Integer(description='Number of users who liked this image'),
    'favorited_by_count': fields.Integer(description='Number of users who favorited this image'),
    'user': fields.Nested(user_ref_model, description='The user who uploaded the image'),
    'tags': fields.List(fields.Nested(tag_ref_model), description='Tags associated with this image'),
    'comments': fields.List(fields.Nested(comment_ref_model), description='Comments on this image'),
    'created_at': fields.DateTime(readonly=True, description='Creation date'),
    'updated_at': fields.DateTime(readonly=True, description='Last update date'),
    'deleted_at': fields.DateTime(description='Deletion date')
})

image_create_model = api.model('ImageCreate', {
    'title': fields.String(required=True, description='The image title'),
    'description': fields.String(description='The image description'),
    'url': fields.String(required=True, description='The image url'),
})

image_update_model = api.model('ImageUpdate', {
    'title': fields.String(description='The new image title'),
    'description': fields.String(description='The new image description'),
    'url': fields.String(required=True, description='The image url'),
})

paginated_images = create_pagination_model('Images', image_model)