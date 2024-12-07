from flask import request
from flask_restx import Namespace, Resource
from app.services.user_service import (
    create_user, get_user, update_user, delete_user, get_user_stats,
    get_user_followers, get_user_following, get_all_users, authenticate_user
)
from app.services.follow_service import follow_user, unfollow_user
from app.schemas import (
    user_model, user_detail_model, pagination_users_model,
    response_message_model, error_model
)

ns = Namespace('users', description='User operations')

@ns.route('')
class UserList(Resource):
    @ns.doc('list_users')
    @ns.marshal_with(pagination_users_model)
    @ns.param('page', 'Page number', type=int, default=1)
    @ns.param('per_page', 'Items per page', type=int, default=20)
    @ns.response(200, 'Success')
    @ns.response(400, 'Bad Request', error_model)
    def get(self):
        """List all users"""
        try:
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 20, type=int)
            users = get_all_users(page, per_page)
            return users, 200
        except ValueError as e:
            ns.abort(400, error=str(e))

    @ns.doc('create_user')
    @ns.expect(user_model)
    @ns.marshal_with(user_detail_model, code=201)
    @ns.response(201, 'User created')
    @ns.response(400, 'Validation Error', error_model)
    def post(self):
        """Create a new user"""
        try:
            new_user = create_user(
                request.json['username'],
                request.json['email'],
                request.json['password'],
                request.json.get('bio')
            )
            return new_user, 201
        except ValueError as e:
            ns.abort(400, error=str(e))

@ns.route('/<int:id>')
@ns.param('id', 'The user identifier')
@ns.response(404, 'User not found', error_model)
class UserResource(Resource):
    @ns.doc('get_user')
    @ns.marshal_with(user_detail_model)
    @ns.response(200, 'Success')
    def get(self, id):
        """Fetch a user given its identifier"""
        user = get_user(id)
        if not user:
            ns.abort(404, error="User not found")
        stats = get_user_stats(id)
        user_data = user.__dict__
        user_data.update(stats)
        return user_data, 200

    @ns.doc('update_user')
    @ns.expect(user_model)
    @ns.marshal_with(user_detail_model)
    @ns.response(200, 'Success')
    @ns.response(400, 'Validation Error', error_model)
    def put(self, id):
        """Update a user given its identifier"""
        try:
            user = update_user(
                id,
                request.json.get('username'),
                request.json.get('email'),
                request.json.get('bio'),
                request.json.get('password')
            )
            stats = get_user_stats(id)
            user_data = user.__dict__
            user_data.update(stats)
            return user_data, 200
        except ValueError as e:
            ns.abort(400, error=str(e))

    @ns.doc('delete_user')
    @ns.response(204, 'User deleted')
    @ns.response(404, 'User not found', error_model)
    def delete(self, id):
        """Delete a user given its identifier"""
        try:
            delete_user(id)
            return '', 204
        except ValueError as e:
            ns.abort(404, error=str(e))

@ns.route('/login')
class UserLogin(Resource):
    @ns.doc('login_user')
    @ns.expect(user_model)
    @ns.marshal_with(user_detail_model)
    @ns.response(200, 'Success')
    @ns.response(401, 'Unauthorized', error_model)
    def post(self):
        """Login a user"""
        user = authenticate_user(request.json['username'], request.json['password'])
        if user:
            return user, 200
        else:
            ns.abort(401, error="Invalid username or password")

@ns.route('/<int:id>/follow')
@ns.param('id', 'The user identifier to follow')
class UserFollow(Resource):
    @ns.doc('follow_user')
    @ns.param('follower_id', 'ID of the user following', type=int, required=True)
    @ns.marshal_with(user_detail_model)
    @ns.response(200, 'Success')
    @ns.response(400, 'Validation Error', error_model)
    def post(self, id):
        """Follow a user"""
        follower_id = request.args.get('follower_id', type=int)
        if not follower_id:
            ns.abort(400, error='Follower ID is required')
        try:
            follow_user(follower_id, id)
            return get_user(id), 200
        except ValueError as e:
            ns.abort(400, error=str(e))

    @ns.doc('unfollow_user')
    @ns.param('follower_id', 'ID of the user unfollowing', type=int, required=True)
    @ns.marshal_with(user_detail_model)
    @ns.response(200, 'Success')
    @ns.response(400, 'Validation Error', error_model)
    def delete(self, id):
        """Unfollow a user"""
        follower_id = request.args.get('follower_id', type=int)
        if not follower_id:
            ns.abort(400, error='Follower ID is required')
        try:
            unfollow_user(follower_id, id)
            return get_user(id), 200
        except ValueError as e:
            ns.abort(400, error=str(e))

@ns.route('/<int:id>/followers')
@ns.param('id', 'The user identifier')
class UserFollowers(Resource):
    @ns.doc('get_user_followers')
    @ns.marshal_with(pagination_users_model)
    @ns.param('page', 'Page number', type=int, default=1)
    @ns.param('per_page', 'Items per page', type=int, default=20)
    @ns.response(200, 'Success')
    @ns.response(404, 'User not found', error_model)
    def get(self, id):
        """Get followers of a user"""
        try:
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 20, type=int)
            followers = get_user_followers(id, page, per_page)
            return {
                'items': [follower.follower for follower in followers.items],
                'total': followers.total,
                'page': page,
                'per_page': per_page,
                'total_pages': followers.pages
            }, 200
        except ValueError as e:
            ns.abort(404, error=str(e))

@ns.route('/<int:id>/following')
@ns.param('id', 'The user identifier')
class UserFollowing(Resource):
    @ns.doc('get_user_following')
    @ns.marshal_with(pagination_users_model)
    @ns.param('page', 'Page number', type=int, default=1)
    @ns.param('per_page', 'Items per page', type=int, default=20)
    @ns.response(200, 'Success')
    @ns.response(404, 'User not found', error_model)
    def get(self, id):
        """Get users that a user is following"""
        try:
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 20, type=int)
            following = get_user_following(id, page, per_page)
            return {
                'items': [follow.followed for follow in following.items],
                'total': following.total,
                'page': page,
                'per_page': per_page,
                'total_pages': following.pages
            }, 200
        except ValueError as e:
            ns.abort(404, error=str(e))
