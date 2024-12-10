from flask import request, abort
from flask_restx import Resource, Namespace 
from flask_jwt_extended import create_access_token
from app.services.user_services import (
    get_user_by_id, get_user_by_username, get_all_users, 
    search_users, create_user, update_user, delete_user,
    verify_user_password, change_user_password
)
from app.schemas.user_schemas import (
    user_model, user_create_model, user_update_model, 
    user_delete_model, user_change_password_model, 
    user_login_model, user_register_model, paginated_users
)
from app.services.image_services import get_images_by_user
from app.schemas.image_schemas import paginated_images
from app.utils.auth_utils import login_required
from app.utils.route_utils import user_exists, error_handler
from .pagination import pagination_parser, search_pagination_parser

ns = Namespace('users', description='User operations')

@ns.route('/')
class UserList(Resource):
    @ns.doc('list_users')
    @ns.expect(pagination_parser)
    @ns.marshal_with(paginated_users)
    @error_handler(400, "ERROR IN UserList.get")
    def get(self):
        """List all users with pagination"""
        args = pagination_parser.parse_args()
        users, count, more = get_all_users(**args)
        return {'results': users, 'count': count, 'more': more}

    @ns.doc('create_user')
    @ns.expect(user_create_model)
    @ns.marshal_with(user_model, code=201)
    @error_handler(400, "ERROR IN UserList.post")
    def post(self):
        """Create a new user"""
        return create_user(**request.json), 201

@ns.route('/<int:uid>')
@ns.param('uid', 'The user identifier')
class UserResource(Resource):
    @ns.doc('get_user')
    @ns.marshal_with(user_model)
    @login_required
    @user_exists
    @error_handler(400, "ERROR IN UserResource.get")
    def get(self, uid):
        """Fetch a user given its identifier"""
        return get_user_by_id(uid)

    @ns.doc('update_user')
    @ns.expect(user_update_model)
    @ns.marshal_with(user_model)
    @login_required
    @user_exists
    @error_handler(400, "ERROR IN UserResource.put")
    def put(self, uid):
        """Update a user given its identifier"""
        return update_user(uid=uid, **request.json)

    @ns.doc('delete_user')
    @ns.expect(user_delete_model)
    @login_required
    @user_exists
    @error_handler(400, "ERROR IN UserResource.delete")
    def delete(self, uid):
        """Delete a user given its identifier"""
        delete_user(uid)
        return '', 204

@ns.route('/<int:uid>/change-password')
@ns.param('uid', 'The user identifier')
class UserChangePassword(Resource):
    @ns.doc('change_password')
    @ns.expect(user_change_password_model)
    @login_required
    @user_exists
    @error_handler(400, "ERROR IN UserChangePassword.post")
    def post(self, uid):
        """Change user password"""
        change_user_password(uid=uid, **request.json)
        return {'message': 'Password changed successfully'}, 200

@ns.route('/<int:uid>/images')
@ns.param('uid', 'The user identifier')
class UserImages(Resource):
    @ns.doc('get_user_images')
    @ns.expect(pagination_parser)
    @ns.marshal_with(paginated_images)
    @user_exists
    @error_handler(400, "ERROR IN UserImages.get")
    def get(self, uid):
        """Get all images uploaded by a specific user"""
        args = pagination_parser.parse_args()
        images, total_count, has_more = get_images_by_user(uid, **args)
        return {
            'results': images,
            'count': total_count,
            'more': has_more
        }

@ns.route('/login')
class UserLogin(Resource):
    @ns.doc('user_login')
    @ns.expect(user_login_model)
    @error_handler(400, "ERROR IN UserLogin.post")
    def post(self):
        """User login"""
        data = request.json
        user = get_user_by_username(data['username'])
        if user and verify_user_password(user, data['password']):
            access_token = create_access_token(identity=str(user.id))
            return {'uid': user.id, 'access_token': access_token}, 200
        abort(401, 'Invalid username or password')

@ns.route('/register')
class UserRegister(Resource):
    @ns.doc('user_register')
    @ns.expect(user_register_model)
    @ns.marshal_with(user_model, code=201)
    @error_handler(400, "ERROR IN UserRegister.post")
    def post(self):
        """Register a new user"""
        return create_user(**request.json), 201

@ns.route('/search')
class SearchUsers(Resource):
    @ns.doc('search_users')
    @ns.expect(search_pagination_parser)
    @ns.marshal_with(paginated_users)
    @error_handler(400, "ERROR IN SearchUsers.get")
    def get(self):
        """Search users by keyword"""
        args = search_pagination_parser.parse_args()
        users, count, more = search_users(**args)
        return {'results': users, 'count': count, 'more': more}