from flask_restx import fields
from app import api
from .pagination import create_pagination_model

# User model
user_model = api.model('User', {
    'id': fields.Integer(readonly=True, description='The user unique identifier'),
    'username': fields.String(required=True, description='The user username'),
    'email': fields.String(required=True, description='The user email'),
    'password_hash': fields.String(required=True, description='The hashed password', attribute='password_hash'),
    'bio': fields.String(description='The user bio'),
    'follower_count': fields.Integer(description='Number of followers'),
    'following_count': fields.Integer(description='Number of users being followed'),
    'image_count': fields.Integer(description='Number of images uploaded'),
    'comment_count': fields.Integer(description='Number of comments made'),
    'collection_count': fields.Integer(description='Number of collections created'),
    'tag_count': fields.Integer(description='Number of tags created'),
    'liked_image_count': fields.Integer(description='Number of images liked'),
    'favorited_image_count': fields.Integer(description='Number of images favorited'),
    'ignored_tag_count': fields.Integer(description='Number of tags ignored'),
    'last_login': fields.DateTime(description='Last login date'),
    'created_at': fields.DateTime(readonly=True, description='Creation date'),
    'updated_at': fields.DateTime(readonly=True, description='Last update date'),
    'deleted_at': fields.DateTime(description='Deletion date')
})

# User creation model
user_create_model = api.model('UserCreate', {
    'username': fields.String(required=True, description='The user username'),
    'email': fields.String(required=True, description='The user email'),
    'password': fields.String(required=True, description='The user password'),
    'bio': fields.String(description='The user bio')
})

# User update model
user_update_model = api.model('UserUpdate', {
    'username': fields.String(description='The user username'),
    'email': fields.String(description='The user email'),
    'password': fields.String(description='The user password'),
    'bio': fields.String(description='The user bio')
})

# User delete model
user_delete_model = api.model('UserDelete', {
    'password': fields.String(required=True, description='The user password')
})

# User login model
user_login_model = api.model('UserLogin', {
    'username': fields.String(required=True, description='The user username'),
    'password': fields.String(required=True, description='The user password')
})

user_register_model = api.model('UserRegister', {
    'username': fields.String(required=True, description='The user username'),
    'email': fields.String(required=True, description='The user email'),
    'password': fields.String(required=True, description='The user password'),
    'bio': fields.String(description='The user bio')
})

user_change_password_model = api.model('UserChangePassword', {
    'old_password': fields.String(required=True, description='The user old password'),
    'new_password': fields.String(required=True, description='The user new password')
})

# Paginated users model
paginated_users = create_pagination_model('Users', user_model)