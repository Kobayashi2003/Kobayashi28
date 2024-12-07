from flask import request, send_file
from flask_restx import Namespace, Resource
from werkzeug.datastructures import FileStorage
from app.services.image_service import (
    create_image, get_image, update_image, delete_image, get_user_images,
    get_feed_images, search_images, get_trending_images, get_all_images
)
from app.services.like_service import like_image, unlike_image, get_user_liked_images
from app.schemas import (
    image_model, image_detail_model, image_input_model, pagination_images_model,
    response_message_model, error_model
)
from app.utils.file_utils import get_image_path

ns = Namespace('images', description='Image operations')

upload_parser = ns.parser()
upload_parser.add_argument('file', location='files', type=FileStorage, required=True)
upload_parser.add_argument('title', location='form', type=str, required=True)
upload_parser.add_argument('description', location='form', type=str, required=False)
upload_parser.add_argument('tags', location='form', type=str, action='split', required=False)

@ns.route('')
class ImageList(Resource):
    @ns.doc('list_images')
    @ns.marshal_with(pagination_images_model)
    @ns.param('page', 'Page number', type=int, default=1)
    @ns.param('per_page', 'Items per page', type=int, default=20)
    @ns.param('sort_by', 'Sort by (created_at or likes)', default='created_at')
    @ns.param('order', 'Sort order (asc or desc)', default='desc')
    @ns.param('tag', 'Filter by tag')
    @ns.param('min_likes', 'Minimum number of likes', type=int)
    @ns.response(200, 'Success')
    @ns.response(400, 'Bad Request', error_model)
    def get(self):
        """List all images"""
        try:
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 20, type=int)
            sort_by = request.args.get('sort_by', 'created_at')
            order = request.args.get('order', 'desc')
            tag = request.args.get('tag')
            min_likes = request.args.get('min_likes', 0, type=int)
            
            images = get_all_images(page, per_page, sort_by, order, tag, min_likes)
            return images, 200
        except ValueError as e:
            ns.abort(400, error=str(e))

    @ns.doc('create_image')
    @ns.expect(upload_parser)
    @ns.marshal_with(image_detail_model, code=201)
    @ns.response(201, 'Image created')
    @ns.response(400, 'Validation Error', error_model)
    def post(self):
        """Create a new image"""
        try:
            args = upload_parser.parse_args()
            user_id = args.get('user_id')
            if not user_id:
                ns.abort(400, error="User ID is required")
            
            new_image = create_image(
                int(user_id),
                args['title'],
                args.get('description', ''),
                args.get('tags', []),
                args['file']
            )
            return new_image, 201
        except ValueError as e:
            ns.abort(400, error=str(e))

@ns.route('/<int:id>')
@ns.param('id', 'The image identifier')
@ns.response(404, 'Image not found', error_model)
class ImageResource(Resource):
    @ns.doc('get_image')
    @ns.marshal_with(image_detail_model)
    @ns.response(200, 'Success')
    def get(self, id):
        """Fetch an image given its identifier"""
        image = get_image(id)
        if not image:
            ns.abort(404, error="Image not found")
        return image, 200

    @ns.doc('update_image')
    @ns.expect(image_input_model)
    @ns.marshal_with(image_detail_model)
    @ns.response(200, 'Success')
    @ns.response(400, 'Validation Error', error_model)
    @ns.response(404, 'Image not found', error_model)
    def put(self, id):
        """Update an image given its identifier"""
        try:
            user_id = 1  # TODO: Replace with authenticated user's ID
            updated_image = update_image(id, user_id, request.json.get('title'), request.json.get('description'), request.json.get('tags'))
            if not updated_image:
                ns.abort(404, error="Image not found")
            return updated_image, 200
        except ValueError as e:
            ns.abort(400, error=str(e))

@ns.route('/<int:id>/file')
@ns.param('id', 'The image identifier')
@ns.response(404, 'Image not found', error_model)
class ImageFile(Resource):
    @ns.doc('get_image_file')
    @ns.response(200, 'Success')
    def get(self, id):
        """Get the image file"""
        image = get_image(id)
        if not image:
            ns.abort(404, error="Image not found")
        file_path = get_image_path(id)
        return send_file(file_path, mimetype='image/jpeg')

@ns.route('/<int:id>/like')
@ns.param('id', 'The image identifier')
class ImageLike(Resource):
    @ns.doc('like_image')
    @ns.param('user_id', 'ID of the user liking the image', type=int, required=True)
    @ns.marshal_with(image_model)
    @ns.response(200, 'Success')
    @ns.response(400, 'Validation Error', error_model)
    @ns.response(404, 'Image not found', error_model)
    def post(self, id):
        """Like an image"""
        user_id = request.args.get('user_id', type=int)
        if not user_id:
            ns.abort(400, error='User ID is required')
        try:
            liked_image = like_image(user_id, id)
            if not liked_image:
                ns.abort(404, error="Image not found")
            return liked_image, 200
        except ValueError as e:
            ns.abort(400, error=str(e))

    @ns.doc('unlike_image')
    @ns.param('user_id', 'ID of the user unliking the image', type=int, required=True)
    @ns.marshal_with(image_model)
    @ns.response(200, 'Success')
    @ns.response(400, 'Validation Error', error_model)
    @ns.response(404, 'Image not found', error_model)
    def delete(self, id):
        """Unlike an image"""
        user_id = request.args.get('user_id', type=int)
        if not user_id:
            ns.abort(400, error='User ID is required')
        try:
            unliked_image = unlike_image(user_id, id)
            if not unliked_image:
                ns.abort(404, error="Image not found")
            return unliked_image, 200
        except ValueError as e:
            ns.abort(400, error=str(e))

@ns.route('/user/<int:user_id>')
@ns.param('user_id', 'The user identifier')
class UserImages(Resource):
    @ns.doc('get_user_images')
    @ns.marshal_with(pagination_images_model)
    @ns.param('page', 'Page number', type=int, default=1)
    @ns.param('per_page', 'Items per page', type=int, default=20)
    @ns.response(200, 'Success')
    @ns.response(404, 'User not found', error_model)
    def get(self, user_id):
        """Get images uploaded by a user"""
        try:
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 20, type=int)
            images = get_user_images(user_id, page, per_page)
            return images, 200
        except ValueError as e:
            ns.abort(404, error=str(e))

@ns.route('/user/<int:user_id>/liked')
@ns.param('user_id', 'The user identifier')
class UserLikedImages(Resource):
    @ns.doc('get_user_liked_images')
    @ns.marshal_with(pagination_images_model)
    @ns.param('page', 'Page number', type=int, default=1)
    @ns.param('per_page', 'Items per page', type=int, default=20)
    @ns.response(200, 'Success')
    @ns.response(404, 'User not found', error_model)
    def get(self, user_id):
        """Get images liked by a user"""
        try:
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 20, type=int)
            images = get_user_liked_images(user_id, page, per_page)
            return images, 200
        except ValueError as e:
            ns.abort(404, error=str(e))

@ns.route('/feed/<int:user_id>')
@ns.param('user_id', 'The user identifier')
class FeedImages(Resource):
    @ns.doc('get_feed_images')
    @ns.marshal_with(pagination_images_model)
    @ns.param('page', 'Page number', type=int, default=1)
    @ns.param('per_page', 'Items per page', type=int, default=20)
    @ns.response(200, 'Success')
    @ns.response(404, 'User not found', error_model)
    def get(self, user_id):
        """Get feed images for a user"""
        try:
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 20, type=int)
            images = get_feed_images(user_id, page, per_page)
            return images, 200
        except ValueError as e:
            ns.abort(404, error=str(e))

@ns.route('/search')
class SearchImages(Resource):
    @ns.doc('search_images')
    @ns.marshal_with(pagination_images_model)
    @ns.param('query', 'Search query', required=True)
    @ns.param('page', 'Page number', type=int, default=1)
    @ns.param('per_page', 'Items per page', type=int, default=20)
    @ns.response(200, 'Success')
    @ns.response(400, 'Bad Request', error_model)
    def get(self):
        """Search images"""
        try:
            query = request.args.get('query', '')
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 20, type=int)
            images = search_images(query, page, per_page)
            return images, 200
        except ValueError as e:
            ns.abort(400, error=str(e))

@ns.route('/trending')
class TrendingImages(Resource):
    @ns.doc('get_trending_images')
    @ns.marshal_with(pagination_images_model)
    @ns.param('time_period', 'Time period (day, week, month)', default='day')
    @ns.param('page', 'Page number', type=int, default=1)
    @ns.param('per_page', 'Items per page', type=int, default=20)
    @ns.response(200, 'Success')
    @ns.response(400, 'Bad Request', error_model)
    def get(self):
        """Get trending images"""
        try:
            time_period = request.args.get('time_period', 'day')
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 20, type=int)
            images = get_trending_images(time_period, page, per_page)
            return images, 200
        except ValueError as e:
            ns.abort(400, error=str(e))
