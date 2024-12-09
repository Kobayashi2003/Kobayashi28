from flask_restx import fields
from app import api
from .common import timestamp_fields, create_pagination_model, user_ref_model
from .tag import tag_ref_model

# Image model
image_model = api.model('Image', {
    'id': fields.Integer(readonly=True, description='The image unique identifier'),
    'title': fields.String(required=True, description='The image title'),
    'description': fields.String(description='The image description'),
    'uid': fields.Integer(required=True, description='The user ID who uploaded the image'),
    'comment_count': fields.Integer(description='Number of comments on this image'),
    'tag_count': fields.Integer(description='Number of tags on this image'),
    'collection_count': fields.Integer(description='Number of collections containing this image'),
    'liked_by_count': fields.Integer(description='Number of users who liked this image'),
    'favorited_by_count': fields.Integer(description='Number of users who favorited this image'),
    'user': fields.Nested(user_ref_model, description='The user who uploaded the image'),
    'tags': fields.List(fields.Nested(tag_ref_model), description='Tags associated with this image'),
    **timestamp_fields
})

# Image creation model
image_create_model = api.model('ImageCreate', {
    'title': fields.String(required=True, description='The image title'),
    'description': fields.String(description='The image description'),
    'user_id': fields.Integer(required=True, description='The user ID uploading the image'),
    'file': fields.Raw(required=True, description='The image file to upload')
})

# Image update model
image_update_model = api.model('ImageUpdate', {
    'title': fields.String(description='The new image title'),
    'description': fields.String(description='The new image description')
})

# Paginated images model
paginated_images = create_pagination_model('Images', image_model)

# Popular image model
popular_image_model = api.model('PopularImage', {
    'image': fields.Nested(image_model),
    'like_count': fields.Integer(description='Number of likes for this image')
})

# Image reference model (for when you need to reference an image in another model)
image_ref_model = api.model('ImageReference', {
    'id': fields.Integer(readonly=True, description='The image unique identifier'),
    'title': fields.String(description='The image title')
})

