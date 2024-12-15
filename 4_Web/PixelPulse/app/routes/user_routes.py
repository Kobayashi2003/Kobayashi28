from flask import request, abort
from flask_restx import Resource, Namespace 
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
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
    @jwt_required
    @user_exists
    @error_handler(400, "ERROR IN UserResource.get")
    def get(self, uid):
        """Fetch a user given its identifier"""
        if uid != get_jwt_identity():
            abort(403, description="You don't have permission to perform this action.")
        return get_user_by_id(uid)

    @ns.doc('update_user')
    @ns.expect(user_update_model)
    @ns.marshal_with(user_model)
    @jwt_required
    @user_exists
    @error_handler(400, "ERROR IN UserResource.put")
    def put(self, uid):
        """Update a user given its identifier"""
        if uid != get_jwt_identity():
            abort(403, description="You don't have permission to perform this action.")
        return update_user(uid=uid, **request.json)

    @ns.doc('delete_user')
    @ns.expect(user_delete_model)
    @jwt_required
    @user_exists
    @error_handler(400, "ERROR IN UserResource.delete")
    def delete(self, uid):
        """Delete a user given its identifier"""
        if uid != get_jwt_identity():
            abort(403, description="You don't have permission to perform this action.")
        delete_user(uid)
        return '', 204

@ns.route('/<int:uid>/change-password')
@ns.param('uid', 'The user identifier')
class UserChangePassword(Resource):
    @ns.doc('change_password')
    @ns.expect(user_change_password_model)
    @jwt_required
    @user_exists
    @error_handler(400, "ERROR IN UserChangePassword.post")
    def post(self, uid):
        """Change user password"""
        if uid != get_jwt_identity():
            abort(403, description="You don't have permission to perform this action.")
        change_user_password(uid=uid, **request.json)
        return {'message': 'Password changed successfully'}, 200

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