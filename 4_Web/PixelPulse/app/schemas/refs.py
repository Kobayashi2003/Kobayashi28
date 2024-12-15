from flask_restx import fields
from app import api

user_ref_model = api.model('UserReference', {
    'id': fields.Integer(readonly=True, description='The user unique identifier'),
    'username': fields.String(description='The user username')
})

image_ref_model = api.model('ImageReference', {
    'id': fields.Integer(readonly=True, description='The image unique identifier'),
    'title': fields.String(description='The image title')
})

tag_ref_model = api.model('TagReference', {
    'id': fields.Integer(readonly=True, description='The tag unique identifier')
})

comment_ref_model = api.model('CommentReference', {
    'id': fields.Integer(readonly=True, description='The comment unique identifier')
})