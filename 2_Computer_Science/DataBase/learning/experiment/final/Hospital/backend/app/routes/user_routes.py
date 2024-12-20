from flask_restx import Namespace, Resource 
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from app.services.user_services import (
    get_user_by_id, get_user_by_username, get_all_users,
    create_user, update_user, delete_user, change_user_password, search_users,
    create_admin, is_admin, grant_admin_privileges, revoke_admin_privileges
) 
from app.schemas.user_schemas import (
    user_model, user_create_model, user_update_model,
    user_login_model, user_register_model, 
    user_change_password_model, paginated_users,
    grant_admin_model, revoke_admin_model,
)
from .pagination import pagination_parser, search_pagination_parser
from app.utils.auth_utils import admin_required
from app.utils.route_utils import error_handler

ns = Namespace('users', description='User operations')

@ns.route('/')
@ns.response(400, 'Bad Request')
@ns.response(403, 'Permission denied')
@ns.response(500, 'Internal Server Error')
class UserList(Resource):
    @ns.doc('list_users')
    @ns.expect(pagination_parser)
    @ns.marshal_list_with(paginated_users)
    @jwt_required()
    @admin_required
    @error_handler(500, "ERROR IN UserListResource.get")
    def get(self):
        """List all users (admin only)"""
        args = pagination_parser.parse_args()
        users, count, more = get_all_users(**args)
        return {'results': users, 'count': count, 'more': more}

    @ns.doc('create_admin')
    @ns.expect(user_create_model)
    @ns.marshal_with(user_model, code=201)
    @ns.response(201, "Registration successful")
    @jwt_required()
    @admin_required
    @error_handler(500, "ERROR IN UserList.post")
    def post(self):
        """Register a new admin user"""
        success, result = create_admin(**ns.payload)
        if success:
            return result, 201
        ns.abort(400, result)

@ns.route('/<int:id>')
@ns.param('id', 'The user identifier')
@ns.response(400, 'Bad Request')
@ns.response(403, 'Permission denied')
@ns.response(404, 'User not found')
@ns.response(500, 'Internal Server Error')
class UserResource(Resource):
    @ns.doc('get_user')
    @ns.marshal_with(user_model)
    @jwt_required()
    @admin_required
    @error_handler(500, "ERROR IN UserResource.get")
    def get(self, id):
        """Fetch a user given its identifier"""
        user = get_user_by_id(id)
        if not user:
            ns.abort(404, "User not found")
        return user

    @ns.doc('update_user')
    @ns.expect(user_update_model)
    @ns.marshal_with(user_model)
    @jwt_required()
    @admin_required
    @error_handler(500, "ERROR IN UserResource.put")
    def put(self, id):
        """Update a user given its identifier"""
        success, result = update_user(id, **ns.payload)
        if not success:
            if result == "User not found":
                ns.abort(404, result)
            else:
                ns.abort(400, result)
        return result

    @ns.doc('delete_user')
    @ns.response(204, 'User deleted')
    @jwt_required()
    @admin_required
    @error_handler(500, "ERROR IN UserResource.delete")
    def delete(self, id):
        """Delete a user given its identifier"""
        success, result = delete_user(id)
        if not success:
            if result == "User not found":
                ns.abort(404, result)
            else:
                ns.abort(400, result)
        return '', 204

@ns.route('/<int:id>/change_password')
@ns.param('id', 'The user identifier')
@ns.response(400, 'Bad Request')
@ns.response(403, 'Permission denied')
@ns.response(500, 'Internal Server Error')
class ChangeUserPassword(Resource):
    @ns.doc('change_user_password')
    @ns.expect(user_change_password_model)
    @ns.marshal_with(user_model)
    @jwt_required
    @admin_required
    @error_handler(500, "ERROR IN ChangeUserPassword.post")
    def post(self, id):
        """Change the password of a user given its identifier"""
        success, result = change_user_password(id, **ns.payload)
        if success:
            return result 
        ns.abort(400, result)

@ns.route('/me')
@ns.response(400, 'Bad Request')
@ns.response(500, 'Internal Server Error')
class CurrentUserResource(Resource):
    @ns.doc('get_current_user')
    @ns.marshal_with(user_model)
    @jwt_required()
    @error_handler(500, "ERROR IN CurrentUserResource.get")
    def get(self):
        """Get the current user's information"""
        current_user_id = get_jwt_identity()
        user = get_user_by_id(current_user_id)
        return user

    @ns.doc('update_current_user')
    @ns.expect(user_update_model)
    @ns.marshal_with(user_model)
    @jwt_required()
    @error_handler(500, "ERROR IN CurrentUserResource.put")
    def put(self):
        """Update the current user's information"""
        current_user_id = get_jwt_identity()
        success, result = update_user(current_user_id, **ns.payload)
        if success:
            return result
        ns.abort(400, result)

    @ns.doc('delete_current_user')
    @ns.response(204, 'User deleted')
    @jwt_required()
    @error_handler(500, "ERROR IN CurrentUserResource.delete")
    def delete(self):
        """Delete the current user"""
        current_user_id = get_jwt_identity()
        success, result = delete_user(current_user_id)
        if success:
            return '', 204
        ns.abort(400, result)

@ns.route('/me/change_password')
@ns.response(400, 'Bad Request')
@ns.response(500, 'Internal Server Error')
class ChangeCurrentUserPassword(Resource):
    @ns.doc('change_current_user_password')
    @ns.expect(user_change_password_model)
    @ns.marshal_with(user_model)
    @jwt_required()
    @error_handler(500, "ERROR IN ChangeCurrentUserPassword.post")
    def post(self):
        """Change the current user's password"""
        current_user_id = get_jwt_identity()
        success, result = change_user_password(current_user_id, **ns.payload)
        if success:
            return result 
        ns.abort(400, result)

@ns.route('/register')
@ns.response(201, 'Registration successful')
@ns.response(400, 'Bad Request')
@ns.response(500, 'Internal Server Error')
class Register(Resource):
    @ns.doc('register_user')
    @ns.expect(user_register_model)
    @ns.marshal_with(user_model, code=201)
    @error_handler(500, "ERROR IN Register.post")
    def post(self):
        """Register a new user"""
        success, result = create_user(**ns.payload)
        if success:
            return result, 201
        ns.abort(400, result)

@ns.route('/login')
@ns.response(200, 'Login successful')
@ns.response(400, 'Bad Request')
@ns.response(401, 'Invalid credentials')
@ns.response(500, 'Internal Server Error')
class Login(Resource):
    @ns.doc('login_user')
    @ns.expect(user_login_model)
    @error_handler(500, "ERROR IN Login.post")
    def post(self):
        """Login and receive an access token"""
        user = get_user_by_username(ns.payload['username'])
        if user and user.check_password(ns.payload['password']):
            access_token = create_access_token(identity=str(user.id))
            return {'access_token': access_token}, 200
        ns.abort(401, 'Invalid credentials')

@ns.route('/grant_admin')
@ns.response(400, 'Bad Request')
@ns.response(403, 'Permission denied')
@ns.response(500, 'Internal Server Error')
class GrantAdmin(Resource):
    @ns.doc('grant_admin_privileges')
    @ns.expect(grant_admin_model)
    @ns.marshal_with(user_model)
    @jwt_required()
    @admin_required
    @error_handler(500, "ERROR IN GrantAdmin.post")
    def post(self):
        """Grant admin privileges to a user (admin only)"""
        success, result = grant_admin_privileges(**ns.payload)
        if not success:
            if result == "User not found":
                ns.abort(404, result)
            else:
                ns.abort(400, result)
        return result

@ns.route('/revoke_admin')
@ns.response(400, 'Bad Request')
@ns.response(403, 'Permission denied')
@ns.response(500, 'Internal Server Error')
class RevokeAdmin(Resource):
    @ns.doc('revoke_admin_privileges')
    @ns.expect(revoke_admin_model)
    @ns.marshal_with(user_model)
    @jwt_required()
    @admin_required
    @error_handler(500, "ERROR IN RevokeAdmin.post")
    def post(self):
        """Revoke admin privileges from a user (admin only)"""
        success, result = revoke_admin_privileges(**ns.payload)
        if not success:
            if result == "User not found":
                ns.abort(404, result)
            else:
                ns.abort(400, result)
        return result

@ns.route('/search')
@ns.response(400, 'Bad Request')
@ns.response(403, 'Permission denied')
@ns.response(500, 'Internal Server Error')
class UserSearch(Resource):
    @ns.doc('search_users')
    @ns.expect(search_pagination_parser)
    @ns.marshal_list_with(paginated_users)
    @jwt_required()
    @admin_required
    @error_handler(500, "ERROR IN UserSearch.post")
    def post(self):
        """Search for users"""
        args = search_pagination_parser.parse_args()
        query = args.pop('query')
        users, count, more = search_users(query, **args)
        return {'results': users, 'count': count, 'more': more}