import os
from flask import request
from flask_restx import Resource, Namespace, reqparse
from app import api
from app.services.image_service import (
    create_image, get_image_by_id, update_image, delete_image, get_all_images,
    get_images_by_user, get_popular_images, search_images, get_related_images
)
from app.schemas.image import image_model, image_create_model, image_update_model, paginated_images, popular_image_model
from werkzeug.utils import secure_filename
from app.utils.file_utils import get_image_path

ns = Namespace('images', description='Image operations')

# Pagination parser
pagination_parser = reqparse.RequestParser()
pagination_parser.add_argument('page', type=int, required=False, default=1, help='Page number')
pagination_parser.add_argument('limit', type=int, required=False, default=10, help='Number of items per page')
pagination_parser.add_argument('sort', type=str, required=False, default='id', help='Field to sort by')
pagination_parser.add_argument('reverse', type=bool, required=False, default=False, help='Sort in reverse order')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@ns.route('/')
class ImageList(Resource):
    @ns.doc('list_images')
    @ns.expect(pagination_parser)
    @ns.marshal_with(paginated_images)
    def get(self):
        """List all images with pagination"""
        args = pagination_parser.parse_args()
        try:
            images, total_count, has_more = get_all_images(**args)
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

    @ns.doc('create_image')
    @ns.expect(image_create_model)
    @ns.marshal_with(image_model, code=201)
    def post(self):
        """Create a new image"""
        # Check if all required fields are present
        if 'title' not in request.form or 'user_id' not in request.form or 'file' not in request.files:
            api.abort(400, "Missing required fields")

        title = request.form['title']
        description = request.form.get('description', '')
        user_id = request.form['user_id']
        file = request.files['file']

        # Validate file
        if file.filename == '':
            api.abort(400, "No file selected for uploading")
        if not allowed_file(file.filename):
            api.abort(400, "File type not allowed")

        try:
            # Create new image entry in database
            new_image = create_image(title=title, description=description, user_id=user_id)

            # Save file
            filename = secure_filename(file.filename)
            file_extension = os.path.splitext(filename)[1]
            file_path = get_image_path(new_image.id, file_extension)
            file.save(file_path)

            # Update image record with file path
            new_image = update_image(new_image.id, file_path=file_path)

            return new_image, 201
        except ValueError as e:
            api.abort(400, str(e))

@ns.route('/<int:id>')
@ns.response(404, 'Image not found')
@ns.param('id', 'The image identifier')
class ImageResource(Resource):
    @ns.doc('get_image')
    @ns.marshal_with(image_model)
    def get(self, id):
        """Fetch an image given its identifier"""
        image = get_image_by_id(id)
        if not image:
            api.abort(404, "Image not found")
        return image

    @ns.doc('update_image')
    @ns.expect(image_update_model)
    @ns.marshal_with(image_model)
    def put(self, id):
        """Update an image given its identifier"""
        data = request.json
        try:
            image = update_image(image_id=id, title=data.get('title'), description=data.get('description'))
            return image
        except ValueError as e:
            api.abort(400, str(e))

    @ns.doc('delete_image')
    @ns.response(204, 'Image deleted')
    def delete(self, id):
        """Delete an image given its identifier"""
        try:
            image = get_image_by_id(id)
            if not image:
                api.abort(404, "Image not found")
            file_path = get_image_path(id)
            if os.path.exists(file_path):
                os.remove(file_path)
            delete_image(id)
            return '', 204
        except ValueError as e:
            api.abort(404, str(e))

@ns.route('/user/<int:user_id>')
@ns.response(404, 'User not found')
@ns.param('user_id', 'The user identifier')
class UserImages(Resource):
    @ns.doc('get_user_images')
    @ns.expect(pagination_parser)
    @ns.marshal_with(paginated_images)
    def get(self, user_id):
        """Get all images uploaded by a specific user"""
        args = pagination_parser.parse_args()
        try:
            images, total_count, has_more = get_images_by_user(user_id, **args)
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

@ns.route('/popular')
class PopularImages(Resource):
    @ns.doc('get_popular_images')
    @ns.marshal_list_with(popular_image_model)
    def get(self):
        """Get the most popular images"""
        return get_popular_images()

@ns.route('/search')
class SearchImages(Resource):
    @ns.doc('search_images')
    @ns.expect(pagination_parser.copy().add_argument('query', type=str, required=True, help='Search query'))
    @ns.marshal_with(paginated_images)
    def get(self):
        """Search for images based on title or description"""
        args = pagination_parser.parse_args()
        query = args.pop('query')
        try:
            images, total_count, has_more = search_images(query, page=args['page'], limit=args['limit'])
        except ValueError as e:
            api.abort(400, str(e))
        
        return {
            'items': images,
            'metadata': {
                'page': args['page'],
                'limit': args['limit'],
                'more': has_more,
                'count': total_count
            }
        }

@ns.route('/<int:id>/related')
@ns.response(404, 'Image not found')
@ns.param('id', 'The image identifier')
class RelatedImages(Resource):
    @ns.doc('get_related_images')
    @ns.marshal_list_with(image_model)
    def get(self, id):
        """Get related images based on common tags"""
        try:
            related_images = get_related_images(id)
            return [image for image, _ in related_images]
        except ValueError as e:
            api.abort(404, str(e))

api.add_namespace(ns)
