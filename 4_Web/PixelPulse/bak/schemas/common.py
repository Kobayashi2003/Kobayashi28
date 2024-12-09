from flask_restx import fields
from app import api

# Updated Pagination metadata model
pagination_model = api.model('PaginationMetadata', {
    'page': fields.Integer(description='Current page number'),
    'limit': fields.Integer(description='Number of items per page'),
    'sort': fields.String(description='Field used for sorting'),
    'reverse': fields.Boolean(description='Whether the sort is in reverse order'),
    'more': fields.Boolean(description='Whether there are more items available'),
    'count': fields.Integer(description='Total number of items')
})

# Function to create paginated models
def create_pagination_model(name, model):
    return api.model(f'Paginated{name}', {
        'items': fields.List(fields.Nested(model)),
        'metadata': fields.Nested(pagination_model)
    })

# Timestamp fields that can be reused in multiple models
timestamp_fields = {
    'created_at': fields.DateTime(readonly=True, description='Creation date'),
    'updated_at': fields.DateTime(readonly=True, description='Last update date')
}

# Basic user reference model (for when you need to reference a user in another model)
user_ref_model = api.model('UserReference', {
    'id': fields.Integer(readonly=True, description='The user unique identifier'),
    'username': fields.String(description='The user username')
})
