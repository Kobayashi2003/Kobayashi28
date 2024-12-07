from flask import request
from flask_restx import Namespace, Resource
from app.services.collection_service import (
    create_collection, get_collection, update_collection, delete_collection,
    add_image_to_collection, remove_image_from_collection,
    get_user_collections, get_collection_images, get_collection_stats,
    get_all_collections
)
from app.schemas import (
    collection_model, collection_input_model, image_model,
    pagination_collections_model, pagination_images_model,
    response_message_model, error_model
)

ns = Namespace('collections', description='Collection operations')

@ns.route('')
class CollectionList(Resource):
    @ns.doc('list_collections')
    @ns.marshal_with(pagination_collections_model)
    @ns.param('page', 'Page number', type=int, default=1)
    @ns.param('per_page', 'Items per page', type=int, default=20)
    @ns.response(200, 'Success')
    @ns.response(400, 'Bad Request', error_model)
    def get(self):
        """List all collections"""
        try:
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 20, type=int)
            collections = get_all_collections(page, per_page)
            return collections, 200
        except ValueError as e:
            ns.abort(400, error=str(e))

    @ns.doc('create_collection')
    @ns.expect(collection_input_model)
    @ns.marshal_with(collection_model, code=201)
    @ns.response(201, 'Collection created')
    @ns.response(400, 'Validation Error', error_model)
    @ns.response(404, 'User not found', error_model)
    def post(self):
        """Create a new collection"""
        try:
            new_collection = create_collection(request.json['user_id'], request.json['name'], request.json.get('description', ''))
            return new_collection, 201
        except ValueError as e:
            ns.abort(400, error=str(e))

@ns.route('/<int:id>')
@ns.param('id', 'The collection identifier')
@ns.response(404, 'Collection not found', error_model)
class CollectionResource(Resource):
    @ns.doc('get_collection')
    @ns.marshal_with(collection_model)
    @ns.response(200, 'Success')
    def get(self, id):
        """Fetch a collection given its identifier"""
        collection = get_collection(id)
        if not collection:
            ns.abort(404, error="Collection not found")
        return collection, 200

    @ns.doc('update_collection')
    @ns.expect(collection_input_model)
    @ns.marshal_with(collection_model)
    @ns.response(200, 'Success')
    @ns.response(400, 'Validation Error', error_model)
    @ns.response(404, 'Collection not found', error_model)
    def put(self, id):
        """Update a collection given its identifier"""
        try:
            updated_collection = update_collection(id, request.json['user_id'], request.json.get('name'), request.json.get('description'))
            if not updated_collection:
                ns.abort(404, error="Collection not found")
            return updated_collection, 200
        except ValueError as e:
            ns.abort(400, error=str(e))

    @ns.doc('delete_collection')
    @ns.response(204, 'Collection deleted')
    @ns.response(400, 'Bad Request', error_model)
    @ns.response(404, 'Collection not found', error_model)
    @ns.param('user_id', 'ID of the user trying to delete the collection', type=int, required=True)
    def delete(self, id):
        """Delete a collection given its identifier"""
        user_id = request.args.get('user_id', type=int)
        if not user_id:
            ns.abort(400, error='User ID is required')
        try:
            delete_collection(id, user_id)
            return '', 204
        except ValueError as e:
            ns.abort(404, error=str(e))

@ns.route('/<int:collection_id>/images')
class CollectionImages(Resource):
    @ns.doc('get_collection_images')
    @ns.marshal_with(pagination_images_model)
    @ns.param('page', 'Page number', type=int, default=1)
    @ns.param('per_page', 'Items per page', type=int, default=20)
    @ns.response(200, 'Success')
    @ns.response(404, 'Collection not found', error_model)
    def get(self, collection_id):
        """Get images in a collection"""
        try:
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 20, type=int)
            images = get_collection_images(collection_id, page, per_page)
            return images, 200
        except ValueError as e:
            ns.abort(404, error=str(e))

    @ns.doc('add_image_to_collection')
    @ns.expect(image_model)
    @ns.marshal_with(collection_model)
    @ns.response(200, 'Success')
    @ns.response(400, 'Validation Error', error_model)
    @ns.response(404, 'Collection, User or Image not found', error_model)
    def post(self, collection_id):
        """Add an image to a collection"""
        try:
            updated_collection = add_image_to_collection(request.json['user_id'], collection_id, request.json['id'])
            return updated_collection, 200
        except ValueError as e:
            ns.abort(404, error=str(e))

    @ns.doc('remove_image_from_collection')
    @ns.expect(image_model)
    @ns.marshal_with(collection_model)
    @ns.response(200, 'Success')
    @ns.response(400, 'Validation Error', error_model)
    @ns.response(404, 'Collection, User or Image not found', error_model)
    def delete(self, collection_id):
        """Remove an image from a collection"""
        try:
            updated_collection = remove_image_from_collection(request.json['user_id'], collection_id, request.json['id'])
            return updated_collection, 200
        except ValueError as e:
            ns.abort(404, error=str(e))

@ns.route('/user/<int:user_id>')
class UserCollections(Resource):
    @ns.doc('get_user_collections')
    @ns.marshal_with(pagination_collections_model)
    @ns.param('page', 'Page number', type=int, default=1)
    @ns.param('per_page', 'Items per page', type=int, default=20)
    @ns.response(200, 'Success')
    @ns.response(404, 'User not found', error_model)
    def get(self, user_id):
        """Get collections of a user"""
        try:
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 20, type=int)
            collections = get_user_collections(user_id, page, per_page)
            return collections, 200
        except ValueError as e:
            ns.abort(404, error=str(e))

@ns.route('/<int:collection_id>/stats')
class CollectionStats(Resource):
    @ns.doc('get_collection_stats')
    @ns.marshal_with(response_message_model)
    @ns.response(200, 'Success')
    @ns.response(404, 'Collection not found', error_model)
    def get(self, collection_id):
        """Get statistics for a collection"""
        try:
            stats = get_collection_stats(collection_id)
            return {'message': stats}, 200
        except ValueError as e:
            ns.abort(404, error=str(e))
