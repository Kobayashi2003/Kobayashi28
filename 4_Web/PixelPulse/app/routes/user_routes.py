from flask import request, abort
from flask_restx import Resource, Namespace 
from flask_jwt_extended import create_access_token 
from app.services.user_services import (
    get_user_by_id, get_user_by_username, get_all_users, 
    create_user, update_user, change_user_password, delete_user,
    verify_user_password
)
from app.schemas.user_schemas import (
    user_model, user_create_model, user_update_model, 
    user_delete_model, user_change_password_model, 
    user_login_model, user_register_model, paginated_users
)
from app.utils.auth_utils import login_required
from .pagination import pagination_parser

ns = Namespace('users', description='User operations')

@ns.errorhandler(Exception)
def handle_exception(error):
    return {'message': str(error)}, 500

@ns.route('/')
class UserList(Resource):
    @ns.doc('list_users')
    @ns.expect(pagination_parser)
    @ns.marshal_with(paginated_users)
    def get(self):
        """List all users with pagination"""
        args = pagination_parser.parse_args()
        page = args['page']
        limit = args['limit']
        sort = args['sort']
        reverse = args['reverse']
        users, count, more = get_all_users(page, limit, sort, reverse)
        return {
            'results': users,
            'count': count,
            'more': more
        }

    @ns.doc('create_user')
    @ns.expect(user_create_model)
    @ns.marshal_with(user_model, code=201)
    def post(self):
        """Create a new user"""
        data = request.json
        new_user = create_user(
            username=data['username'],
            email=data['email'],
            password=data['password'],
            bio=data['bio']
        )
        return new_user, 201

@ns.route('/<int:uid>')
@ns.param('uid', 'The user identifier')
class UserResource(Resource):
    @ns.doc('get_user')
    @ns.marshal_with(user_model)
    @login_required
    def get(self, uid):
        """Fetch a user given its identifier"""
        user = get_user_by_id(uid)
        return user

    @ns.doc('update_user')
    @ns.expect(user_update_model)
    @ns.marshal_with(user_model)
    @login_required
    def put(self, uid):
        """Update a user given its identifier"""
        data = request.json
        user = update_user(
            uid=uid,
            username=data.get('username'),
            email=data.get('email'),
            bio=data.get('bio')
        )
        return user

    @ns.doc('delete_user')
    @ns.expect(user_delete_model)
    @ns.response(204, 'User deleted')
    @login_required
    def delete(self, uid):
        """Delete a user given its identifier"""
        delete_user(uid)
        return '', 204

    @ns.route('/<int:uid>/change-password')
    @ns.param('uid', 'The user identifier')
    class UserChangePassword(Resource):
        @ns.doc('change_password')
        @ns.expect(user_change_password_model)
        @ns.response(200, 'Password changed successfully')
        @ns.response(400, 'Invalid input')
        @ns.response(401, 'Unauthorized')
        @login_required
        def post(self, uid):
            """Change user password"""
            data = request.json
            change_user_password(
                uid=uid,
                old_password=data['old_password'],
                new_password=data['new_password']
            )
            return '', 200

@ns.route('/login')
class UserLogin(Resource):
    @ns.doc('user_login')
    @ns.expect(user_login_model)
    @ns.response(200, 'Login successful')
    @ns.response(401, 'Invalid username or password')
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
    @ns.response(400, 'Invalid input')
    def post(self):
        """Register a new user"""
        data = request.json
        new_user = create_user(
            username=data['username'],
            email=data['email'],
            password=data['password'],
            bio=data.get('bio', '')
        )
        return new_user, 201