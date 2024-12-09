from flask import request
from flask_restx import Resource, Namespace, reqparse
from app import api
from app.services.comment_service import (
    create_comment, get_comment_by_id, update_comment, delete_comment,
    get_comments_by_image, get_comments_by_user, get_replies,
    get_comment_count, is_comment_owner
)
from app.schemas.comment import comment_model, comment_create_model, comment_update_model, paginated_comments

ns = Namespace('comments', description='Comment operations')

# Pagination parser
pagination_parser = reqparse.RequestParser()
pagination_parser.add_argument('page', type=int, required=False, default=1, help='Page number')
pagination_parser.add_argument('limit', type=int, required=False, default=10, help='Number of items per page')
pagination_parser.add_argument('sort', type=str, required=False, default='created_at', help='Field to sort by')
pagination_parser.add_argument('reverse', type=bool, required=False, default=True, help='Sort in reverse order')

@ns.route('/')
class CommentList(Resource):
    @ns.doc('create_comment')
    @ns.expect(comment_create_model)
    @ns.marshal_with(comment_model, code=201)
    def post(self):
        """Create a new comment"""
        data = request.json
        try:
            new_comment = create_comment(
                content=data['content'],
                user_id=data['user_id'],
                image_id=data['image_id'],
                parent_id=data.get('parent_id')
            )
            return new_comment, 201
        except ValueError as e:
            api.abort(400, str(e))

@ns.route('/<int:id>')
@ns.response(404, 'Comment not found')
@ns.param('id', 'The comment identifier')
class CommentResource(Resource):
    @ns.doc('get_comment')
    @ns.marshal_with(comment_model)
    def get(self, id):
        """Fetch a comment given its identifier"""
        comment = get_comment_by_id(id)
        if not comment:
            api.abort(404, "Comment not found")
        return comment

    @ns.doc('update_comment')
    @ns.expect(comment_update_model)
    @ns.marshal_with(comment_model)
    def put(self, id):
        """Update a comment given its identifier"""
        data = request.json
        try:
            comment = update_comment(comment_id=id, content=data['content'])
            return comment
        except ValueError as e:
            api.abort(400, str(e))

    @ns.doc('delete_comment')
    @ns.response(204, 'Comment deleted')
    def delete(self, id):
        """Delete a comment given its identifier"""
        try:
            delete_comment(id)
            return '', 204
        except ValueError as e:
            api.abort(404, str(e))

@ns.route('/image/<int:image_id>')
@ns.response(404, 'Image not found')
@ns.param('image_id', 'The image identifier')
class ImageComments(Resource):
    @ns.doc('get_image_comments')
    @ns.expect(pagination_parser)
    @ns.marshal_with(paginated_comments)
    def get(self, image_id):
        """Get all comments for a specific image"""
        args = pagination_parser.parse_args()
        try:
            comments, total_count, has_more = get_comments_by_image(image_id, **args)
        except ValueError as e:
            api.abort(400, str(e))
        
        return {
            'items': comments,
            'metadata': {
                'page': args['page'],
                'limit': args['limit'],
                'sort': args['sort'],
                'reverse': args['reverse'],
                'more': has_more,
                'count': total_count
            }
        }

@ns.route('/user/<int:user_id>')
@ns.response(404, 'User not found')
@ns.param('user_id', 'The user identifier')
class UserComments(Resource):
    @ns.doc('get_user_comments')
    @ns.expect(pagination_parser)
    @ns.marshal_with(paginated_comments)
    def get(self, user_id):
        """Get all comments made by a specific user"""
        args = pagination_parser.parse_args()
        try:
            comments, total_count, has_more = get_comments_by_user(user_id, **args)
        except ValueError as e:
            api.abort(400, str(e))
        
        return {
            'items': comments,
            'metadata': {
                'page': args['page'],
                'limit': args['limit'],
                'sort': args['sort'],
                'reverse': args['reverse'],
                'more': has_more,
                'count': total_count
            }
        }

@ns.route('/<int:comment_id>/replies')
@ns.response(404, 'Comment not found')
@ns.param('comment_id', 'The comment identifier')
class CommentReplies(Resource):
    @ns.doc('get_comment_replies')
    @ns.expect(pagination_parser)
    @ns.marshal_with(paginated_comments)
    def get(self, comment_id):
        """Get all replies to a specific comment"""
        args = pagination_parser.parse_args()
        try:
            replies, total_count, has_more = get_replies(comment_id, **args)
        except ValueError as e:
            api.abort(400, str(e))
        
        return {
            'items': replies,
            'metadata': {
                'page': args['page'],
                'limit': args['limit'],
                'sort': args['sort'],
                'reverse': args['reverse'],
                'more': has_more,
                'count': total_count
            }
        }

@ns.route('/image/<int:image_id>/count')
@ns.response(404, 'Image not found')
@ns.param('image_id', 'The image identifier')
class CommentCount(Resource):
    @ns.doc('get_comment_count')
    def get(self, image_id):
        """Get the number of comments for a specific image"""
        count = get_comment_count(image_id)
        return {'count': count}

api.add_namespace(ns)

