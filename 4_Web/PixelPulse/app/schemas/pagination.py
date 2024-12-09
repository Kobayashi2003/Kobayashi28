from flask_restx import fields
from app import api

# Function to create paginated models
def create_pagination_model(name, model):
    return api.model(f'Paginated{name}', {
        'results': fields.List(fields.Nested(model)),
        'more': fields.Boolean(description='Whether there are more items available'),
        'count': fields.Integer(description='Total number of items')
    })
