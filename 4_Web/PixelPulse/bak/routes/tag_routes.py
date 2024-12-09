from flask import request
from flask_restx import Resource, Namespace, reqparse
from app import api
from app.services.tag_service import (
    create_tag, get_tag_by_id, update_tag, delete_tag, get_all_tags,
    get_tags_by_user, get_popular_tags, add_tag_to_image, remove_tag_from_image,
    get_images_by_tag, search_tags
)
from app.schemas.tag import tag_model, tag_create_model, tag_update_model, paginated_tags, popular_tag_model

ns = Namespace('tags', description='Tag operations')

# Pagination parser
pagination_parser = reqparse.RequestParser()
pagination_parser.add_argument('page', type=int, required=False, default=1, help='Page number')
pagination_parser.add_argument('limit', type=int, required=False, default=10, help='Number of items per page')
pagination_parser.add_argument('sort', type=str, required=False, default='id', help='Field to sort by')
pagination_parser.add_argument('reverse', type=bool, required=False, default=False, help='Sort in reverse order')

@ns.route('/')
class TagList(Resource):
    @ns.doc('list_tags')
    @ns.expect(pagination_parser)
    @ns.marshal_with(paginated_tags)
    def get(self):
        """List all tags with pagination"""
        args = pagination_parser.parse_args()
        try:
            tags, total_count, has_more = get_all_tags(**args)
        except ValueError as e:
            api.abort(400, str(e))
        
        return {
            'items': tags,
            'metadata': {
                'page': args['page'],
                'limit': args['limit'],
                'sort': args['sort'],
                'reverse': args['reverse'],
                'more': has_more,
                'count': total_count
            }
        }

    @ns.doc('create_tag')
    @ns.expect(tag_create_model)
    @ns.marshal_with(tag_model, code=201)
    def post(self):
        """Create a new tag"""
        data = request.json
        try:
            new_tag = create_tag(name=data['name'], user_id=data['user_id'])
            return new_tag, 201
        except ValueError as e:
            api.abort(400, str(e))

@ns.route('/<int:id>')
@ns.response(404, 'Tag not found')
@ns.param('id', 'The tag identifier')
class TagResource(Resource):
    @ns.doc('get_tag')
    @ns.marshal_with(tag_model)
    def get(self, id):
        """Fetch a tag given its identifier"""
        tag = get_tag_by_id(id)
        if not tag:
            api.abort(404, "Tag not found")
        return tag

    @ns.doc('update_tag')
    @ns.expect(tag_update_model)
    @ns.marshal_with(tag_model)
    def put(self, id):
        """Update a tag given its identifier"""
        data = request.json
        try:
            tag = update_tag(tag_id=id, name=data['name'])
            return tag
        except ValueError as e:
            api.abort(400, str(e))

    @ns.doc('delete_tag')
    @ns.response(204, 'Tag deleted')
    def delete(self, id):
        """Delete a tag given its identifier"""
        try:
            delete_tag(id)
            return '', 204
        except ValueError as e:
            api.abort(404, str(e))

@ns.route('/user/<int:user_id>')
@ns.response(404, 'User not found')
@ns.param('user_id', 'The user identifier')
class UserTags(Resource):
    @ns.doc('get_user_tags')
    @ns.expect(pagination_parser)
    @ns.marshal_with(paginated_tags)
    def get(self, user_id):
        """Get all tags created by a specific user"""
        args = pagination_parser.parse_args()
        try:
            tags, total_count, has_more = get_tags_by_user(user_id, **args)
        except ValueError as e:
            api.abort(400, str(e))
        
        return {
            'items': tags,
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
class PopularTags(Resource):
    @ns.doc('get_popular_tags')
    @ns.marshal_list_with(popular_tag_model)
    def get(self):
        """Get the most popular tags"""
        return get_popular_tags()

@ns.route('/<int:tag_id>/images')
@ns.response(404, 'Tag not found')
@ns.param('tag_id', 'The tag identifier')
class TagImages(Resource):
    @ns.doc('get_images_by_tag')
    @ns.expect(pagination_parser)
    @ns.marshal_with(paginated_tags)  # This should be changed to paginated_images when available
    def get(self, tag_id):
        """Get all images associated with a specific tag"""
        args = pagination_parser.parse_args()
        try:
            images, total_count, has_more = get_images_by_tag(tag_id, **args)
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

@ns.route('/search')
class SearchTags(Resource):
    @ns.doc('search_tags')
    @ns.expect(pagination_parser.copy().add_argument('query', type=str, required=True, help='Search query'))
    @ns.marshal_with(paginated_tags)
    def get(self):
        """Search for tags based on a query string"""
        args = pagination_parser.parse_args()
        query = args.pop('query')
        try:
            tags, total_count, has_more = search_tags(query, **args)
        except ValueError as e:
            api.abort(400, str(e))
        
        return {
            'items': tags,
            'metadata': {
                'page': args['page'],
                'limit': args['limit'],
                'sort': args['sort'],
                'reverse': args['reverse'],
                'more': has_more,
                'count': total_count
            }
        }

@ns.route('/<int:tag_id>/image/<int:image_id>')
@ns.response(404, 'Tag or Image not found')
@ns.param('tag_id', 'The tag identifier')
@ns.param('image_id', 'The image identifier')
class TagImageAssociation(Resource):
    @ns.doc('add_tag_to_image')
    @ns.response(204, 'Tag added to image')
    def post(self, tag_id, image_id):
        """Add a tag to an image"""
        try:
            add_tag_to_image(tag_id, image_id)
            return '', 204
        except ValueError as e:
            api.abort(404, str(e))

    @ns.doc('remove_tag_from_image')
    @ns.response(204, 'Tag removed from image')
    def delete(self, tag_id, image_id):
        """Remove a tag from an image"""
        try:
            remove_tag_from_image(tag_id, image_id)
            return '', 204
        except ValueError as e:
            api.abort(404, str(e))

api.add_namespace(ns)
