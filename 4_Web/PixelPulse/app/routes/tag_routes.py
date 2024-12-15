from flask import request
from flask_restx import Resource, Namespace
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.tag_services import (
    get_tag_by_id, get_all_tags, get_tags_by_user,
    serach_tags, create_tag, update_tag, delete_tag,
    add_tag_to_image, remove_tag_from_image, get_images_by_tag 
)
from app.schemas.tag_schemas import (
    tag_model, tag_create_model,
    tag_update_model, paginated_tags
)
from app.utils.route_utils import (
    user_exists, image_exists, 
    tag_exists, error_handler 
)
from .pagination import pagination_parser, search_pagination_parser

from .user_routes import ns as user_ns
from .image_routes import ns as image_ns

ns = Namespace('tags', description='Tag operations') 

@ns.route('/')
class TagList(Resource):
    @ns.doc('list_tags')
    @ns.expect(pagination_parser)
    @ns.marshal_with(paginated_tags)
    @error_handler(400, "ERROR IN TagList.get")
    def get(self):
        """List all tags with pagination"""
        args = pagination_parser.parse_args()
        tags, count, more = get_all_tags(**args)
        return {'results': tags, 'count': count, 'more': more}

    @ns.doc('create_tag')
    @ns.expect(tag_create_model)
    @ns.marshal_with(tag_model, code=201)
    @jwt_required
    @error_handler(400, "ERROR IN TagList.post")
    def post(self):
        """Create a new tag"""
        uid = int(get_jwt_identity())
        return create_tag(uid=uid, **request.json), 201

@ns.route('/<int:id>') 
@ns.param('id', 'The tag identifier')
class TagResource(Resource):
    @ns.doc('get_tag')
    @ns.marshal_with(tag_model)
    @tag_exists
    @error_handler(400, "ERROR IN TagResource.get")
    def get(self, id):
        """Fetch a tag given its identifier"""
        return get_tag_by_id(id)

    @ns.doc('update_tag') 
    @ns.expect(tag_update_model)
    @ns.marshal_with(tag_model)
    @jwt_required
    @tag_exists
    @error_handler(400, "ERROR IN TagResource.post")
    def post(self, id):
        """Update a tag given its identifier"""
        uid = int(get_jwt_identity())
        return update_tag(id=id, uid=uid, **request.json)

    @ns.doc('delete_tag')  
    @jwt_required
    @tag_exists
    @error_handler(400, "ERROR IN TagResource.delete")
    def delete(self, id):
        """Delete a tag given its identifier"""
        uid = int(get_jwt_identity())
        delete_tag(id=id, uid=uid)
        return '', 204

@ns.route('/search') 
class SearchTags(Resource):
    @ns.doc('search_tags')
    @ns.expect(search_pagination_parser)
    @ns.marshal_with(paginated_tags)
    @error_handler(400, "ERROR IN SearchTags.get")
    def get(self):
        """Search tags by keyword"""
        args = search_pagination_parser.parse_args()
        tags, count, more = serach_tags(**args)
        return {'results': tags, 'count': count, 'more': more}

@user_ns.route('/<int:uid>/tags')
@user_ns.param('uid', 'The user identifier')
class UserTags(Resource):
    @user_ns.doc('get_user_tags')
    @user_ns.expect(pagination_parser)
    @user_ns.marshal_with(paginated_tags)
    @user_exists
    @error_handler(400, "ERROR IN UserTags.get")
    def get(self, uid):
        """Get all tags created by a specific user"""
        args = pagination_parser.parse_args()
        tags, count, more = get_tags_by_user(uid, **args) 
        return {'results': tags, 'count': count, 'more': more}        
