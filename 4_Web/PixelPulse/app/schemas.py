from flask_restx import fields
from app import api

# Basic models
user_model = api.model('User', {
    'id': fields.Integer(readonly=True),
    'username': fields.String(required=True),
    'email': fields.String(required=True),
    'bio': fields.String,
    'created_at': fields.DateTime(readonly=True)
})

tag_model = api.model('Tag', {
    'id': fields.Integer(readonly=True),
    'name': fields.String(required=True),
    'creator_id': fields.Integer(readonly=True),
    'created_at': fields.DateTime(readonly=True),
    'image_count': fields.Integer(readonly=True)
})

image_model = api.model('Image', {
    'id': fields.Integer(readonly=True),
    'title': fields.String(required=True),
    'description': fields.String,
    'created_at': fields.DateTime(readonly=True),
    'tags': fields.List(fields.Nested(tag_model)),
    'like_count': fields.Integer(readonly=True),
    'comment_count': fields.Integer(readonly=True),
    'collection_count': fields.Integer(readonly=True)
})

comment_model = api.model('Comment', {
    'id': fields.Integer(readonly=True),
    'content': fields.String(required=True),
    'created_at': fields.DateTime(readonly=True),
    'updated_at': fields.DateTime(readonly=True),
    'user_id': fields.Integer(required=True),
    'image_id': fields.Integer(required=True)
})

collection_model = api.model('Collection', {
    'id': fields.Integer(readonly=True),
    'name': fields.String(required=True),
    'description': fields.String,
    'created_at': fields.DateTime(readonly=True),
    'is_default': fields.Boolean(readonly=True),
    'user_id': fields.Integer(required=True)
})

# Extended models
user_detail_model = api.model('UserDetail', {
    'id': fields.Integer(readonly=True),
    'username': fields.String(required=True),
    'email': fields.String(required=True),
    'bio': fields.String,
    'created_at': fields.DateTime(readonly=True),
    'image_count': fields.Integer(readonly=True),
    'liked_image_count': fields.Integer(readonly=True),
    'follower_count': fields.Integer(readonly=True),
    'following_count': fields.Integer(readonly=True)
})

image_detail_model = api.model('ImageDetail', {
    'id': fields.Integer(readonly=True),
    'title': fields.String(required=True),
    'description': fields.String,
    'created_at': fields.DateTime(readonly=True),
    'tags': fields.List(fields.Nested(tag_model)),
    'like_count': fields.Integer(readonly=True),
    'comment_count': fields.Integer(readonly=True),
    'collection_count': fields.Integer(readonly=True),
    'user': fields.Nested(user_model),
    'comments': fields.List(fields.Nested(comment_model))
})

collection_detail_model = api.model('CollectionDetail', {
    'id': fields.Integer(readonly=True),
    'name': fields.String(required=True),
    'description': fields.String,
    'created_at': fields.DateTime(readonly=True),
    'is_default': fields.Boolean(readonly=True),
    'user_id': fields.Integer(required=True),
    'image_count': fields.Integer(readonly=True),
    'images': fields.List(fields.Nested(image_model))
})

# Pagination models
pagination_model = api.model('PaginatedResult', {
    'items': fields.List(fields.Raw),
    'total': fields.Integer,
    'page': fields.Integer,
    'per_page': fields.Integer,
    'total_pages': fields.Integer
})

pagination_users_model = api.inherit('PaginatedUsers', pagination_model, {
    'items': fields.List(fields.Nested(user_model))
})

pagination_images_model = api.inherit('PaginatedImages', pagination_model, {
    'items': fields.List(fields.Nested(image_model))
})

pagination_comments_model = api.inherit('PaginatedComments', pagination_model, {
    'items': fields.List(fields.Nested(comment_model))
})

pagination_collections_model = api.inherit('PaginatedCollections', pagination_model, {
    'items': fields.List(fields.Nested(collection_model))
})

pagination_tags_model = api.inherit('PaginatedTags', pagination_model, {
    'items': fields.List(fields.Nested(tag_model))
})

# Input models
image_input_model = api.model('ImageInput', {
    'title': fields.String(required=True),
    'description': fields.String,
    'tags': fields.List(fields.String)
})

comment_input_model = api.model('CommentInput', {
    'content': fields.String(required=True)
})

collection_input_model = api.model('CollectionInput', {
    'name': fields.String(required=True),
    'description': fields.String
})

# Response models
response_message_model = api.model('ResponseMessage', {
    'message': fields.String
})

error_model = api.model('ErrorModel', {
    'error': fields.String
})

