from flask_restx import fields
from app import api
from .common import timestamp_fields, create_pagination_model, user_ref_model

# Collection model
collection_model = api.model('Collection', {
    'id': fields.Integer(readonly=True, description='The collection unique identifier'),
    'name': fields.String(required=True, description='The collection name'),
    'description': fields.String(description='The collection description'),
    'uid': fields.Integer(required=True, description='The user ID who created the collection'),
    'is_default': fields.Boolean(description='Whether this is the default collection'),
    'image_count': fields.Integer(description='Number of images in this collection'),
    'user': fields.Nested(user_ref_model, description='The user who created the collection'),
    **timestamp_fields
})

# Collection creation model
collection_create_model = api.model('CollectionCreate', {
    'name': fields.String(required=True, description='The collection name'),
    'description': fields.String(description='The collection description'),
    'user_id': fields.Integer(required=True, description='The user ID creating the collection'),
    'is_default': fields.Boolean(description='Whether this is the default collection')
})

# Collection update model
collection_update_model = api.model('CollectionUpdate', {
    'name': fields.String(description='The new collection name'),
    'description': fields.String(description='The new collection description')
})

# Paginated collections model
paginated_collections = create_pagination_model('Collections', collection_model)

# Collection reference model (for when you need to reference a collection in another model)
collection_ref_model = api.model('CollectionReference', {
    'id': fields.Integer(readonly=True, description='The collection unique identifier'),
    'name': fields.String(description='The collection name')
})
