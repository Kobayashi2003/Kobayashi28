from flask_restx import fields
from app import api
from .pagination import create_pagination_model

user_model = api.model('User', {
    'id': fields.Integer(readonly=True, description='The user unique identifier'),
    'is_admin': fields.Boolean(description='Whether the user is an admin'),
    'username': fields.String(required=True, description='The user username'),
    'phone_number': fields.String(required=True, description='The user phone number'),
    'password_hash': fields.String(required=True, description='The hashed password', attribute='password_hash'),
    'bio': fields.String(description='The user bio'),
    'created_at': fields.DateTime(readonly=True, description='Creation date'),
    'updated_at': fields.DateTime(readonly=True, description='Last update date')
})

user_create_model = api.model('UserCreate', {
    'username': fields.String(required=True, description='The user username'),
    'phone_number': fields.String(required=True, description='The user phone number'),
    'password': fields.String(required=True, description='The user password'),
    'bio': fields.String(description='The user bio')
})

user_update_model = api.model('UserUpdate', {
    'username': fields.String(description='The user username'),
    'phone_number': fields.String(description='The user phone number'),
    'bio': fields.String(description='The user bio')
})

user_login_model = api.model('UserLogin', {
    'username': fields.String(required=True, description='The user username'),
    'password': fields.String(required=True, description='The user password')
})

user_register_model = api.model('UserRegister', {
    'username': fields.String(required=True, description='The user username'),
    'phone_number': fields.String(required=True, description='The user phone number'),
    'password': fields.String(required=True, description='The user password'),
    'bio': fields.String(description='The user bio')
})

user_change_password_model = api.model('UserChangePassword', {
    'old_password': fields.String(required=True, description='The user old password'),
    'new_password': fields.String(required=True, description='The user new password')
})

grant_admin_model = api.model('GrantAdmin', {
    'user_id': fields.Integer(required=True, description='The ID of the user to grant admin privileges'),
    'admin_password': fields.String(required=True, description='The admin password for verification')
})

revoke_admin_model = api.model('RevokeAdmin', {
    'user_id': fields.Integer(required=True, description='The ID of the user to revoke admin privileges'),
    'admin_password': fields.String(required=True, description='The admin password for verification')
})

paginated_users = create_pagination_model('Users', user_model)