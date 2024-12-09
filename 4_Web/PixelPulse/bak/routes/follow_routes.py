from flask import request
from flask_restx import Resource, Namespace, reqparse
from app import api
from app.services.follow_service import (
    follow_user, unfollow_user, get_user_followers, get_user_following,
    is_following, get_follower_count, get_following_count
)
from app.schemas.user import paginated_users

ns = Namespace('follows', description='Follow operations')

# Pagination parser
pagination_parser = reqparse.RequestParser()
pagination_parser.add_argument('page', type=int, required=False, default=1, help='Page number')
pagination_parser.add_argument('limit', type=int, required=False, default=10, help='Number of items per page')
pagination_parser.add_argument('sort', type=str, required=False, default='username', help='Field to sort by')
pagination_parser.add_argument('reverse', type=bool, required=False, default=False, help='Sort in reverse order')

@ns.route('/<int:follower_id>/<int:followed_id>')
@ns.response(404, 'User not found')
@ns.param('follower_id', 'The follower user identifier')
@ns.param('followed_id', 'The followed user identifier')
class FollowResource(Resource):
    @ns.doc('follow_user')
    @ns.response(204, 'User followed')
    def post(self, follower_id, followed_id):
        """Follow a user"""
        try:
            follow_user(follower_id, followed_id)
            return '', 204
        except ValueError as e:
            api.abort(400, str(e))

    @ns.doc('unfollow_user')
    @ns.response(204, 'User unfollowed')
    def delete(self, follower_id, followed_id):
        """Unfollow a user"""
        try:
            unfollow_user(follower_id, followed_id)
            return '', 204
        except ValueError as e:
            api.abort(400, str(e))

@ns.route('/<int:user_id>/followers')
@ns.response(404, 'User not found')
@ns.param('user_id', 'The user identifier')
class UserFollowers(Resource):
    @ns.doc('get_user_followers')
    @ns.expect(pagination_parser)
    @ns.marshal_with(paginated_users)
    def get(self, user_id):
        """Get all followers of a user"""
        args = pagination_parser.parse_args()
        try:
            followers, total_count, has_more = get_user_followers(user_id, **args)
        except ValueError as e:
            api.abort(400, str(e))
        
        return {
            'items': followers,
            'metadata': {
                'page': args['page'],
                'limit': args['limit'],
                'sort': args['sort'],
                'reverse': args['reverse'],
                'more': has_more,
                'count': total_count
            }
        }

@ns.route('/<int:user_id>/following')
@ns.response(404, 'User not found')
@ns.param('user_id', 'The user identifier')
class UserFollowing(Resource):
    @ns.doc('get_user_following')
    @ns.expect(pagination_parser)
    @ns.marshal_with(paginated_users)
    def get(self, user_id):
        """Get all users followed by a user"""
        args = pagination_parser.parse_args()
        try:
            following, total_count, has_more = get_user_following(user_id, **args)
        except ValueError as e:
            api.abort(400, str(e))
        
        return {
            'items': following,
            'metadata': {
                'page': args['page'],
                'limit': args['limit'],
                'sort': args['sort'],
                'reverse': args['reverse'],
                'more': has_more,
                'count': total_count
            }
        }

@ns.route('/<int:follower_id>/<int:followed_id>/check')
@ns.response(404, 'User not found')
@ns.param('follower_id', 'The follower user identifier')
@ns.param('followed_id', 'The followed user identifier')
class CheckFollowing(Resource):
    @ns.doc('is_following')
    def get(self, follower_id, followed_id):
        """Check if a user is following another user"""
        try:
            following = is_following(follower_id, followed_id)
            return {'following': following}
        except ValueError as e:
            api.abort(404, str(e))

@ns.route('/<int:user_id>/follower_count')
@ns.response(404, 'User not found')
@ns.param('user_id', 'The user identifier')
class FollowerCount(Resource):
    @ns.doc('get_follower_count')
    def get(self, user_id):
        """Get the number of followers for a user"""
        try:
            count = get_follower_count(user_id)
            return {'count': count}
        except ValueError as e:
            api.abort(404, str(e))

@ns.route('/<int:user_id>/following_count')
@ns.response(404, 'User not found')
@ns.param('user_id', 'The user identifier')
class FollowingCount(Resource):
    @ns.doc('get_following_count')
    def get(self, user_id):
        """Get the number of users a user is following"""
        try:
            count = get_following_count(user_id)
            return {'count': count}
        except ValueError as e:
            api.abort(404, str(e))

api.add_namespace(ns)

