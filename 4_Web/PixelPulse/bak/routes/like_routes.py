from flask import request
from flask_restx import Resource, Namespace, reqparse
from app import api
from app.services.like_service import (
    like_image, unlike_image, get_liked_images, get_users_who_liked,
    is_image_liked, get_like_count
)
from app.schemas.image import paginated_images
from app.schemas.user import paginated_users

ns = Namespace('likes', description='Like operations')

# Pagination parser
pagination_parser = reqparse.RequestParser()
pagination_parser.add_argument('page', type=int, required=False, default=1, help='Page number')
pagination_parser.add_argument('limit', type=int, required=False, default=10, help='Number of items per page')
pagination_parser.add_argument('sort', type=str, required=False, default='created_at', help='Field to sort by')
pagination_parser.add_argument('reverse', type=bool, required=False, default=True, help='Sort in reverse order')

@ns.route('/user/<int:user_id>/image/<int:image_id>')
@ns.response(404, 'User or Image not found')
@ns.param('user_id', 'The user identifier')
@ns.param('image_id', 'The image identifier')
class LikeResource(Resource):
    @ns.doc('like_image')
    @ns.response(204, 'Image liked')
    def post(self, user_id, image_id):
        """Like an image"""
        try:
            like_image(user_id, image_id)
            return '', 204
        except ValueError as e:
            api.abort(404, str(e))

    @ns.doc('unlike_image')
    @ns.response(204, 'Image unliked')
    def delete(self, user_id, image_id):
        """Unlike an image"""
        try:
            unlike_image(user_id, image_id)
            return '', 204
        except ValueError as e:
            api.abort(404, str(e))

@ns.route('/user/<int:user_id>/liked')
@ns.response(404, 'User not found')
@ns.param('user_id', 'The user identifier')
class UserLikedImages(Resource):
    @ns.doc('get_liked_images')
    @ns.expect(pagination_parser)
    @ns.marshal_with(paginated_images)
    def get(self, user_id):
        """Get all images liked by a specific user"""
        args = pagination_parser.parse_args()
        try:
            images, total_count, has_more = get_liked_images(user_id, **args)
        except ValueError as e:
            api.abort(400, str(e))
        
        return {
            'items': images,
            'metadata': {
                'page': args['page'],
                'limit': args['limit'],
                'sort': args['sort'],
                'reverse': args['reverse'],
                'more': has_more,
                'count': total_count
            }
        }

@ns.route('/image/<int:image_id>/liked_by')
@ns.response(404, 'Image not found')
@ns.param('image_id', 'The image identifier')
class ImageLikedByUsers(Resource):
    @ns.doc('get_users_who_liked')
    @ns.expect(pagination_parser)
    @ns.marshal_with(paginated_users)
    def get(self, image_id):
        """Get all users who liked a specific image"""
        args = pagination_parser.parse_args()
        try:
            users, total_count, has_more = get_users_who_liked(image_id, **args)
        except ValueError as e:
            api.abort(400, str(e))
        
        return {
            'items': users,
            'metadata': {
                'page': args['page'],
                'limit': args['limit'],
                'sort': args['sort'],
                'reverse': args['reverse'],
                'more': has_more,
                'count': total_count
            }
        }

@ns.route('/user/<int:user_id>/image/<int:image_id>/check')
@ns.response(404, 'User or Image not found')
@ns.param('user_id', 'The user identifier')
@ns.param('image_id', 'The image identifier')
class CheckImageLiked(Resource):
    @ns.doc('is_image_liked')
    def get(self, user_id, image_id):
        """Check if a user has liked a specific image"""
        try:
            liked = is_image_liked(user_id, image_id)
            return {'liked': liked}
        except ValueError as e:
            api.abort(404, str(e))

@ns.route('/image/<int:image_id>/count')
@ns.response(404, 'Image not found')
@ns.param('image_id', 'The image identifier')
class LikeCount(Resource):
    @ns.doc('get_like_count')
    def get(self, image_id):
        """Get the number of likes for a specific image"""
        try:
            count = get_like_count(image_id)
            return {'count': count}
        except ValueError as e:
            api.abort(404, str(e))

api.add_namespace(ns)
