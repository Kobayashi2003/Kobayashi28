from flask import request
from flask_restx import Namespace, Resource
from app.services.comment_service import (
    create_comment, get_comment, update_comment, delete_comment,
    get_image_comments, get_user_comments, get_recent_comments,
    search_comments, get_comment_stats, get_all_comments
)
from app.schemas import (
    comment_model, comment_input_model, pagination_comments_model,
    response_message_model, error_model
)

ns = Namespace('comments', description='Comment operations')

@ns.route('')
class CommentList(Resource):
    @ns.doc('list_comments')
    @ns.marshal_with(pagination_comments_model)
    @ns.param('page', 'Page number', type=int, default=1)
    @ns.param('per_page', 'Items per page', type=int, default=20)
    @ns.response(200, 'Success')
    @ns.response(400, 'Bad Request', error_model)
    def get(self):
        """List all comments"""
        try:
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 20, type=int)
            comments = get_all_comments(page, per_page)
            return comments, 200
        except ValueError as e:
            ns.abort(400, error=str(e))

    @ns.doc('create_comment')
    @ns.expect(comment_input_model)
    @ns.marshal_with(comment_model, code=201)
    @ns.response(201, 'Comment created')
    @ns.response(400, 'Validation Error', error_model)
    @ns.response(404, 'User or Image not found', error_model)
    def post(self):
        """Create a new comment"""
        try:
            new_comment = create_comment(request.json['user_id'], request.json['image_id'], request.json['content'])
            return new_comment, 201
        except ValueError as e:
            ns.abort(400, error=str(e))

@ns.route('/<int:id>')
@ns.param('id', 'The comment identifier')
@ns.response(404, 'Comment not found', error_model)
class CommentResource(Resource):
    @ns.doc('get_comment')
    @ns.marshal_with(comment_model)
    @ns.response(200, 'Success')
    def get(self, id):
        """Fetch a comment given its identifier"""
        comment = get_comment(id)
        if not comment:
            ns.abort(404, error="Comment not found")
        return comment, 200

    @ns.doc('update_comment')
    @ns.expect(comment_input_model)
    @ns.marshal_with(comment_model)
    @ns.response(200, 'Success')
    @ns.response(400, 'Validation Error', error_model)
    @ns.response(404, 'Comment not found', error_model)
    def put(self, id):
        """Update a comment given its identifier"""
        try:
            updated_comment = update_comment(id, request.json['user_id'], request.json['content'])
            if not updated_comment:
                ns.abort(404, error="Comment not found")
            return updated_comment, 200
        except ValueError as e:
            ns.abort(400, error=str(e))

    @ns.doc('delete_comment')
    @ns.response(204, 'Comment deleted')
    @ns.response(400, 'Bad Request', error_model)
    @ns.response(404, 'Comment not found', error_model)
    @ns.param('user_id', 'ID of the user trying to delete the comment', type=int, required=True)
    def delete(self, id):
        """Delete a comment given its identifier"""
        user_id = request.args.get('user_id', type=int)
        if not user_id:
            ns.abort(400, error='User ID is required')
        try:
            delete_comment(id, user_id)
            return '', 204
        except ValueError as e:
            ns.abort(404, error=str(e))

@ns.route('/image/<int:image_id>')
class ImageComments(Resource):
    @ns.doc('get_image_comments')
    @ns.marshal_with(pagination_comments_model)
    @ns.param('page', 'Page number', type=int, default=1)
    @ns.param('per_page', 'Items per page', type=int, default=20)
    @ns.response(200, 'Success')
    @ns.response(404, 'Image not found', error_model)
    def get(self, image_id):
        """Get comments for a specific image"""
        try:
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 20, type=int)
            comments = get_image_comments(image_id, page, per_page)
            return comments, 200
        except ValueError as e:
            ns.abort(404, error=str(e))

@ns.route('/user/<int:user_id>')
class UserComments(Resource):
    @ns.doc('get_user_comments')
    @ns.marshal_with(pagination_comments_model)
    @ns.param('page', 'Page number', type=int, default=1)
    @ns.param('per_page', 'Items per page', type=int, default=20)
    @ns.response(200, 'Success')
    @ns.response(404, 'User not found', error_model)
    def get(self, user_id):
        """Get comments made by a specific user"""
        try:
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 20, type=int)
            comments = get_user_comments(user_id, page, per_page)
            return comments, 200
        except ValueError as e:
            ns.abort(404, error=str(e))

@ns.route('/recent')
class RecentComments(Resource):
    @ns.doc('get_recent_comments')
    @ns.marshal_with(pagination_comments_model)
    @ns.param('page', 'Page number', type=int, default=1)
    @ns.param('per_page', 'Items per page', type=int, default=20)
    @ns.response(200, 'Success')
    def get(self):
        """Get recent comments across all images"""
        try:
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 20, type=int)
            comments = get_recent_comments(page, per_page)
            return comments, 200
        except ValueError as e:
            ns.abort(400, error=str(e))

@ns.route('/search')
class SearchComments(Resource):
    @ns.doc('search_comments')
    @ns.marshal_with(pagination_comments_model)
    @ns.param('query', 'Search query', required=True)
    @ns.param('page', 'Page number', type=int, default=1)
    @ns.param('per_page', 'Items per page', type=int, default=20)
    @ns.response(200, 'Success')
    @ns.response(400, 'Bad Request', error_model)
    def get(self):
        """Search comments by content"""
        try:
            query = request.args.get('query', '')
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 20, type=int)
            comments = search_comments(query, page, per_page)
            return comments, 200
        except ValueError as e:
            ns.abort(400, error=str(e))

@ns.route('/stats/<int:image_id>')
class CommentStats(Resource):
    @ns.doc('get_comment_stats')
    @ns.marshal_with(response_message_model)
    @ns.response(200, 'Success')
    @ns.response(404, 'Image not found', error_model)
    def get(self, image_id):
        """Get comment statistics for an image"""
        try:
            stats = get_comment_stats(image_id)
            return {'message': stats}, 200
        except ValueError as e:
            ns.abort(404, error=str(e))
