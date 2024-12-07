from flask import request
from flask_restx import Namespace, Resource
from app.services.tag_service import (
    create_tag, get_tag, get_tag_by_name, update_tag, delete_tag,
    add_tag_to_image, remove_tag_from_image, get_images_by_tag,
    get_popular_tags, ignore_tag, unignore_tag, get_user_ignored_tags,
    get_tag_stats, get_all_tags
)
from app.schemas import (
    tag_model, pagination_tags_model, pagination_images_model,
    response_message_model, error_model
)

ns = Namespace('tags', description='Tag operations')

@ns.route('')
class TagList(Resource):
    @ns.doc('list_tags')
    @ns.marshal_with(pagination_tags_model)
    @ns.param('page', 'Page number', type=int, default=1)
    @ns.param('per_page', 'Items per page', type=int, default=20)
    @ns.response(200, 'Success')
    @ns.response(400, 'Bad Request', error_model)
    def get(self):
        """List all tags"""
        try:
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 20, type=int)
            tags = get_all_tags(page, per_page)
            return tags, 200
        except ValueError as e:
            ns.abort(400, error=str(e))

    @ns.doc('create_tag')
    @ns.expect(tag_model)
    @ns.marshal_with(tag_model)
    @ns.response(201, 'Tag created')
    @ns.response(200, 'Tag already exists')
    @ns.response(400, 'Validation Error', error_model)
    def post(self):
        """Create a new tag"""
        try:
            new_tag, created = create_tag(request.json['name'], request.json['creator_id'])
            return new_tag, 201 if created else 200
        except ValueError as e:
            ns.abort(400, error=str(e))

@ns.route('/<int:id>')
@ns.param('id', 'The tag identifier')
@ns.response(404, 'Tag not found', error_model)
class TagResource(Resource):
    @ns.doc('get_tag')
    @ns.marshal_with(tag_model)
    @ns.response(200, 'Success')
    def get(self, id):
        """Fetch a tag given its identifier"""
        tag = get_tag(id)
        if not tag:
            ns.abort(404, error="Tag not found")
        return tag, 200

    @ns.doc('update_tag')
    @ns.expect(tag_model)
    @ns.marshal_with(tag_model)
    @ns.response(200, 'Success')
    @ns.response(400, 'Validation Error', error_model)
    @ns.response(404, 'Tag not found', error_model)
    def put(self, id):
        """Update a tag given its identifier"""
        try:
            updated_tag = update_tag(id, request.json['name'], request.json['creator_id'])
            if not updated_tag:
                ns.abort(404, error="Tag not found")
            return updated_tag, 200
        except ValueError as e:
            ns.abort(400, error=str(e))

    @ns.doc('delete_tag')
    @ns.response(204, 'Tag deleted')
    @ns.response(400, 'Bad Request', error_model)
    @ns.response(404, 'Tag not found', error_model)
    @ns.param('user_id', 'ID of the user trying to delete the tag', type=int, required=True)
    def delete(self, id):
        """Delete a tag given its identifier"""
        user_id = request.args.get('user_id', type=int)
        if not user_id:
            ns.abort(400, error='User ID is required')
        try:
            delete_tag(id, user_id)
            return '', 204
        except ValueError as e:
            ns.abort(404, error=str(e))

@ns.route('/name/<string:name>')
class TagByNameResource(Resource):
    @ns.doc('get_tag_by_name')
    @ns.marshal_with(tag_model)
    @ns.response(200, 'Success')
    @ns.response(404, 'Tag not found', error_model)
    def get(self, name):
        """Fetch a tag given its name"""
        try:
            tag = get_tag_by_name(name)
            return tag, 200
        except ValueError as e:
            ns.abort(404, error=str(e))

@ns.route('/<int:tag_id>/image/<int:image_id>')
class TagImageAssociation(Resource):
    @ns.doc('add_tag_to_image')
    @ns.marshal_with(tag_model)
    @ns.response(200, 'Success')
    @ns.response(400, 'Bad Request', error_model)
    @ns.response(404, 'Tag or Image not found', error_model)
    def post(self, tag_id, image_id):
        """Add a tag to an image"""
        try:
            updated_tag = add_tag_to_image(tag_id, image_id)
            return updated_tag, 200
        except ValueError as e:
            ns.abort(404, error=str(e))

    @ns.doc('remove_tag_from_image')
    @ns.marshal_with(tag_model)
    @ns.response(200, 'Success')
    @ns.response(400, 'Bad Request', error_model)
    @ns.response(404, 'Tag or Image not found', error_model)
    def delete(self, tag_id, image_id):
        """Remove a tag from an image"""
        try:
            updated_tag = remove_tag_from_image(tag_id, image_id)
            return updated_tag, 200
        except ValueError as e:
            ns.abort(404, error=str(e))

@ns.route('/<int:tag_id>/images')
class TagImages(Resource):
    @ns.doc('get_images_by_tag')
    @ns.marshal_with(pagination_images_model)
    @ns.param('page', 'Page number', type=int, default=1)
    @ns.param('per_page', 'Items per page', type=int, default=20)
    @ns.response(200, 'Success')
    @ns.response(404, 'Tag not found', error_model)
    def get(self, tag_id):
        """Get images associated with a tag"""
        try:
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 20, type=int)
            images = get_images_by_tag(tag_id, page, per_page)
            return images, 200
        except ValueError as e:
            ns.abort(404, error=str(e))

@ns.route('/popular')
class PopularTags(Resource):
    @ns.doc('get_popular_tags')
    @ns.marshal_list_with(tag_model)
    @ns.param('limit', 'Number of popular tags to return', type=int, default=10)
    @ns.response(200, 'Success')
    def get(self):
        """Get popular tags"""
        limit = request.args.get('limit', 10, type=int)
        popular_tags = get_popular_tags(limit)
        return popular_tags, 200

@ns.route('/ignore')
class IgnoreTag(Resource):
    @ns.doc('ignore_tag')
    @ns.expect(tag_model)
    @ns.marshal_with(tag_model)
    @ns.response(200, 'Success')
    @ns.response(400, 'Validation Error', error_model)
    @ns.response(404, 'Tag or User not found', error_model)
    def post(self):
        """Ignore a tag for a user"""
        try:
            ignored_tag = ignore_tag(request.json['user_id'], request.json['id'])
            return ignored_tag, 200
        except ValueError as e:
            ns.abort(404, error=str(e))

    @ns.doc('unignore_tag')
    @ns.expect(tag_model)
    @ns.response(204, 'Tag unignored')
    @ns.response(400, 'Validation Error', error_model)
    @ns.response(404, 'Tag or User not found', error_model)
    def delete(self):
        """Unignore a tag for a user"""
        try:
            unignore_tag(request.json['user_id'], request.json['id'])
            return '', 204
        except ValueError as e:
            ns.abort(404, error=str(e))

@ns.route('/user/<int:user_id>/ignored')
class UserIgnoredTags(Resource):
    @ns.doc('get_user_ignored_tags')
    @ns.marshal_with(pagination_tags_model)
    @ns.param('page', 'Page number', type=int, default=1)
    @ns.param('per_page', 'Items per page', type=int, default=20)
    @ns.response(200, 'Success')
    @ns.response(404, 'User not found', error_model)
    def get(self, user_id):
        """Get tags ignored by a user"""
        try:
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 20, type=int)
            ignored_tags = get_user_ignored_tags(user_id, page, per_page)
            return ignored_tags, 200
        except ValueError as e:
            ns.abort(404, error=str(e))

@ns.route('/<int:tag_id>/stats')
class TagStats(Resource):
    @ns.doc('get_tag_stats')
    @ns.marshal_with(response_message_model)
    @ns.response(200, 'Success')
    @ns.response(404, 'Tag not found', error_model)
    def get(self, tag_id):
        """Get statistics for a tag"""
        try:
            stats = get_tag_stats(tag_id)
            return {'message': stats}, 200
        except ValueError as e:
            ns.abort(404, error=str(e))
