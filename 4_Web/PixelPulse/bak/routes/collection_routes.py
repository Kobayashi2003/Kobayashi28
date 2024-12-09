from flask import request
from flask_restx import Resource, Namespace, reqparse
from app import api
from app.services.collection_service import (
    create_collection, get_collection_by_id, update_collection, delete_collection,
    get_collections_by_user, add_image_to_collection, remove_image_from_collection,
    get_images_in_collection, get_collection_count, is_collection_owner
)
from app.schemas.collection import collection_model, collection_create_model, collection_update_model, paginated_collections
from app.schemas.image import paginated_images

ns = Namespace('collections', description='Collection operations')

# Pagination parser
pagination_parser = reqparse.RequestParser()
pagination_parser.add_argument('page', type=int, required=False, default=1, help='Page number')
pagination_parser.add_argument('limit', type=int, required=False, default=10, help='Number of items per page')
pagination_parser.add_argument('sort', type=str, required=False, default='created_at', help='Field to sort by')
pagination_parser.add_argument('reverse', type=bool, required=False, default=True, help='Sort in reverse order')

@ns.route('/')
class CollectionList(Resource):
    @ns.doc('create_collection')
    @ns.expect(collection_create_model)
    @ns.marshal_with(collection_model, code=201)
    def post(self):
        """Create a new collection"""
        data = request.json
        try:
            new_collection = create_collection(
                name=data['name'],
                description=data.get('description'),
                user_id=data['user_id'],
                is_default=data.get('is_default', False)
            )
            return new_collection, 201
        except ValueError as e:
            api.abort(400, str(e))

@ns.route('/<int:id>')
@ns.response(404, 'Collection not found')
@ns.param('id', 'The collection identifier')
class CollectionResource(Resource):
    @ns.doc('get_collection')
    @ns.marshal_with(collection_model)
    def get(self, id):
        """Fetch a collection given its identifier"""
        collection = get_collection_by_id(id)
        if not collection:
            api.abort(404, "Collection not found")
        return collection

    @ns.doc('update_collection')
    @ns.expect(collection_update_model)
    @ns.marshal_with(collection_model)
    def put(self, id):
        """Update a collection given its identifier"""
        data = request.json
        try:
            collection = update_collection(
                collection_id=id,
                name=data.get('name'),
                description=data.get('description')
            )
            return collection
        except ValueError as e:
            api.abort(400, str(e))

    @ns.doc('delete_collection')
    @ns.response(204, 'Collection deleted')
    def delete(self, id):
        """Delete a collection given its identifier"""
        try:
            delete_collection(id)
            return '', 204
        except ValueError as e:
            api.abort(404, str(e))

@ns.route('/user/<int:user_id>')
@ns.response(404, 'User not found')
@ns.param('user_id', 'The user identifier')
class UserCollections(Resource):
    @ns.doc('get_user_collections')
    @ns.expect(pagination_parser)
    @ns.marshal_with(paginated_collections)
    def get(self, user_id):
        """Get all collections created by a specific user"""
        args = pagination_parser.parse_args()
        try:
            collections, total_count, has_more = get_collections_by_user(user_id, **args)
        except ValueError as e:
            api.abort(400, str(e))
        
        return {
            'items': collections,
            'metadata': {
                'page': args['page'],
                'limit': args['limit'],
                'sort': args['sort'],
                'reverse': args['reverse'],
                'more': has_more,
                'count': total_count
            }
        }

@ns.route('/<int:collection_id>/images')
@ns.response(404, 'Collection not found')
@ns.param('collection_id', 'The collection identifier')
class CollectionImages(Resource):
    @ns.doc('get_collection_images')
    @ns.expect(pagination_parser)
    @ns.marshal_with(paginated_images)
    def get(self, collection_id):
        """Get all images in a specific collection"""
        args = pagination_parser.parse_args()
        try:
            images, total_count, has_more = get_images_in_collection(collection_id, **args)
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

@ns.route('/<int:collection_id>/images/<int:image_id>')
@ns.response(404, 'Collection or Image not found')
@ns.param('collection_id', 'The collection identifier')
@ns.param('image_id', 'The image identifier')
class CollectionImageAssociation(Resource):
    @ns.doc('add_image_to_collection')
    @ns.response(204, 'Image added to collection')
    def post(self, collection_id, image_id):
        """Add an image to a collection"""
        try:
            add_image_to_collection(collection_id, image_id)
            return '', 204
        except ValueError as e:
            api.abort(404, str(e))

    @ns.doc('remove_image_from_collection')
    @ns.response(204, 'Image removed from collection')
    def delete(self, collection_id, image_id):
        """Remove an image from a collection"""
        try:
            remove_image_from_collection(collection_id, image_id)
            return '', 204
        except ValueError as e:
            api.abort(404, str(e))

@ns.route('/user/<int:user_id>/count')
@ns.response(404, 'User not found')
@ns.param('user_id', 'The user identifier')
class CollectionCount(Resource):
    @ns.doc('get_collection_count')
    def get(self, user_id):
        """Get the number of collections for a specific user"""
        count = get_collection_count(user_id)
        return {'count': count}

api.add_namespace(ns)

