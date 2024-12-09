from flask import request
from flask_restx import Resource, Namespace, reqparse
from app import api
from app.services.recommendation_service import (
    get_recommended_images, get_recommended_users, get_recommended_images_after_interaction,
    get_recommended_users_after_follow, get_popular_images, get_trending_users, get_personalized_feed
)
from app.schemas.image import paginated_images
from app.schemas.user import paginated_users

ns = Namespace('recommendations', description='Recommendation operations')

# Pagination parser
pagination_parser = reqparse.RequestParser()
pagination_parser.add_argument('page', type=int, required=False, default=1, help='Page number')
pagination_parser.add_argument('limit', type=int, required=False, default=10, help='Number of items per page')

# Time period parser
time_period_parser = pagination_parser.copy()
time_period_parser.add_argument('time_period', type=str, required=False, default='day', help='Time period for popularity (day, week, month)')

@ns.route('/images/user/<int:user_id>')
@ns.response(404, 'User not found')
@ns.param('user_id', 'The user identifier')
class RecommendedImages(Resource):
    @ns.doc('get_recommended_images')
    @ns.expect(pagination_parser)
    @ns.marshal_with(paginated_images)
    def get(self, user_id):
        """Get recommended images for a user"""
        args = pagination_parser.parse_args()
        try:
            images, total_count, has_more = get_recommended_images(user_id, **args)
        except ValueError as e:
            api.abort(404, str(e))
        
        return {
            'items': images,
            'metadata': {
                'page': args['page'],
                'limit': args['limit'],
                'more': has_more,
                'count': total_count
            }
        }

@ns.route('/users/<int:user_id>')
@ns.response(404, 'User not found')
@ns.param('user_id', 'The user identifier')
class RecommendedUsers(Resource):
    @ns.doc('get_recommended_users')
    @ns.expect(pagination_parser)
    @ns.marshal_with(paginated_users)
    def get(self, user_id):
        """Get recommended users for a user to follow"""
        args = pagination_parser.parse_args()
        try:
            users, total_count, has_more = get_recommended_users(user_id, **args)
        except ValueError as e:
            api.abort(404, str(e))
        
        return {
            'items': users,
            'metadata': {
                'page': args['page'],
                'limit': args['limit'],
                'more': has_more,
                'count': total_count
            }
        }

@ns.route('/images/after_interaction/<int:user_id>/<int:image_id>')
@ns.response(404, 'User or Image not found')
@ns.param('user_id', 'The user identifier')
@ns.param('image_id', 'The image identifier')
class RecommendedImagesAfterInteraction(Resource):
    @ns.doc('get_recommended_images_after_interaction')
    @ns.expect(pagination_parser)
    @ns.marshal_with(paginated_images)
    def get(self, user_id, image_id):
        """Get recommended images after a user interacts with an image"""
        args = pagination_parser.parse_args()
        try:
            images, total_count, has_more = get_recommended_images_after_interaction(user_id, image_id, **args)
        except ValueError as e:
            api.abort(404, str(e))
        
        return {
            'items': images,
            'metadata': {
                'page': args['page'],
                'limit': args['limit'],
                'more': has_more,
                'count': total_count
            }
        }

@ns.route('/users/after_follow/<int:user_id>/<int:followed_user_id>')
@ns.response(404, 'User not found')
@ns.param('user_id', 'The user identifier')
@ns.param('followed_user_id', 'The followed user identifier')
class RecommendedUsersAfterFollow(Resource):
    @ns.doc('get_recommended_users_after_follow')
    @ns.expect(pagination_parser)
    @ns.marshal_with(paginated_users)
    def get(self, user_id, followed_user_id):
        """Get recommended users to follow after a user follows another user"""
        args = pagination_parser.parse_args()
        try:
            users, total_count, has_more = get_recommended_users_after_follow(user_id, followed_user_id, **args)
        except ValueError as e:
            api.abort(404, str(e))
        
        return {
            'items': users,
            'metadata': {
                'page': args['page'],
                'limit': args['limit'],
                'more': has_more,
                'count': total_count
            }
        }

@ns.route('/images/popular')
class PopularImages(Resource):
    @ns.doc('get_popular_images')
    @ns.expect(time_period_parser)
    @ns.marshal_with(paginated_images)
    def get(self):
        """Get popular images"""
        args = time_period_parser.parse_args()
        try:
            images, total_count, has_more = get_popular_images(**args)
        except ValueError as e:
            api.abort(400, str(e))
        
        return {
            'items': images,
            'metadata': {
                'page': args['page'],
                'limit': args['limit'],
                'time_period': args['time_period'],
                'more': has_more,
                'count': total_count
            }
        }

@ns.route('/users/trending')
class TrendingUsers(Resource):
    @ns.doc('get_trending_users')
    @ns.expect(time_period_parser)
    @ns.marshal_with(paginated_users)
    def get(self):
        """Get trending users"""
        args = time_period_parser.parse_args()
        try:
            users, total_count, has_more = get_trending_users(**args)
        except ValueError as e:
            api.abort(400, str(e))
        
        return {
            'items': users,
            'metadata': {
                'page': args['page'],
                'limit': args['limit'],
                'time_period': args['time_period'],
                'more': has_more,
                'count': total_count
            }
        }

@ns.route('/feed/<int:user_id>')
@ns.response(404, 'User not found')
@ns.param('user_id', 'The user identifier')
class PersonalizedFeed(Resource):
    @ns.doc('get_personalized_feed')
    @ns.expect(pagination_parser)
    @ns.marshal_with(paginated_images)
    def get(self, user_id):
        """Get personalized feed for a user"""
        args = pagination_parser.parse_args()
        try:
            images, total_count, has_more = get_personalized_feed(user_id, **args)
        except ValueError as e:
            api.abort(404, str(e))
        
        return {
            'items': images,
            'metadata': {
                'page': args['page'],
                'limit': args['limit'],
                'more': has_more,
                'count': total_count
            }
        }

api.add_namespace(ns)

