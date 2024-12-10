from flask import request 
from flask_restx import Resource, Namespace
from flask_jwt_extended import get_jwt_identity
from app.services.image_services import (
    get_image_by_id, get_all_images, search_images, 
    create_image, update_image, delete_image
)
from app.schemas.image_schemas import (
    image_model, image_create_model, 
    image_update_model, paginated_images
)
from app.utils.auth_utils import login_required
from app.utils.route_utils import image_exists, error_handler
from .pagination import pagination_parser, search_pagination_parser

ns = Namespace('images', description='Image operations')

@ns.route('/')
class ImageList(Resource):
    @ns.doc('list_images')
    @ns.expect(pagination_parser)
    @ns.marshal_with(paginated_images)
    @error_handler(400, "ERROR IN ImageList.get")
    def get(self):
        raise ValueError("This is a test error")
        """List all images with pagination"""
        args = pagination_parser.parse_args()
        images, count, more = get_all_images(**args)
        return {'results': images, 'count': count, 'more': more}

    @ns.doc('create_image')
    @ns.expect(image_create_model)
    @ns.marshal_with(image_model, code=201)
    @login_required
    @error_handler(400, "ERROR IN ImageList.post")
    def post(self):
        """Create a new image"""
        uid = int(get_jwt_identity())
        return create_image(uid=uid, **request.json), 201

@ns.route('/<int:id>')
@ns.param('id', 'The image identifier')
class ImageResource(Resource):
    @ns.doc('get_image')
    @ns.marshal_with(image_model)
    @image_exists
    @error_handler(400, "ERROR IN ImageResource.get")
    def get(self, id):
        """Fetch an image given its identifier"""
        return get_image_by_id(id)

    @ns.doc('update_image')
    @ns.expect(image_update_model)
    @ns.marshal_with(image_model)
    @login_required
    @image_exists
    @error_handler(400, "ERROR IN ImageResource.put")
    def put(self, id):
        """Update an image given its identifier"""
        uid = int(get_jwt_identity())
        return update_image(id=id, uid=uid, **request.json)
    
    @ns.doc('delete_image')
    @login_required
    @image_exists
    @error_handler(400, "ERROR IN ImageResource.delete")
    def delete(self, id):
        """Delete an image given its identifier"""
        uid = int(get_jwt_identity())
        delete_image(id=id, uid=uid)
        return '', 204

@ns.route('/search')
class SearchImages(Resource):
    @ns.doc('search_images')
    @ns.expect(search_pagination_parser)
    @ns.marshal_with(paginated_images)
    @error_handler(400, "ERROR IN SearchImages.get")
    def get(self):
        """Search images by keyword"""
        args = search_pagination_parser.parse_args()
        images, count, more = search_images(**args)
        return {'results': images, 'count': count, 'more': more}