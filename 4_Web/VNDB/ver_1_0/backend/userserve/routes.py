from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token 

api_bp = Blueprint('api', __name__, url_prefix='/')

@api_bp.errorhandler(400)
def bad_request(e):
    return jsonify(error=str(e.description)), 400

@api_bp.errorhandler(404)
def not_found(e):
    return jsonify(error="Resource not found"), 404

@api_bp.errorhandler(500)
def server_error(e):
    return jsonify(error="An unexpected error occurred"), 500

@api_bp.route('', methods=['GET', 'TRACE'])
def hello_world():
    return jsonify({"message": "USERSERVE"})


from .operations import (
    is_marked, create_user, update_user, delete_user, change_password,
    get_category, create_category, update_category, delete_category,
    clear_category, add_mark_to_category, remove_mark_from_category,
    contains_mark, search_categories, get_user_by_username,
    get_marks_from_category_without_pagination, get_categories_by_mark
)


@api_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data['username'].strip()
    password = data['password']
    user = get_user_by_username(username)
    if user and user.check_password(password):
        access_token = create_access_token(identity=user.id)
        return jsonify({
            'access_token':access_token,
            'username': username 
        }), 200
    return jsonify(error="Invalid username or password"), 401

@api_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    user = create_user(data['username'], data['password'])
    if user:
        access_token = create_access_token(identity=user.id)
        return jsonify({
            'access_token':access_token,
            'username': data['username']
        }), 201
    return jsonify(error="Username already exists"), 400


@api_bp.route('/u<username>', methods=['GET'])
@jwt_required()
def get_user_route(username):
    current_user_id = get_jwt_identity()
    user = get_user_by_username(username)
    if not user:
        return jsonify(error="User not found"), 404
    if current_user_id != user.id:
        return jsonify(error="Unauthorized"), 403
    return jsonify(dict(user)), 200

@api_bp.route('/u<username>', methods=['PUT'])
@jwt_required()
def update_user_route(username):
    current_user_id = get_jwt_identity()
    user = get_user_by_username(username)
    if not user:
        return jsonify(error="User not found"), 404
    if current_user_id != user.id:
        return jsonify(error="Unauthorized"), 403
    data = request.json
    user = update_user(user.id, username=data.get('username'))
    if not user:
        return jsonify(error="Update failed"), 400
    return jsonify(dict(user)), 200

@api_bp.route('/u<username>', methods=['DELETE'])
@jwt_required()
def delete_user_route(username):
    current_user_id = get_jwt_identity()
    user = get_user_by_username(username)
    if not user:
        return jsonify(error="User not found"), 404
    if current_user_id != user.id:
        return jsonify(error="Unauthorized"), 403
    if not delete_user(user.id):
        return jsonify(message="Delete failed"), 400
    return jsonify(message="User deleted"), 200

@api_bp.route('/u<uername>/change_password', methods=['POST'])
@jwt_required()
def change_password_route(username):
    current_user_id = get_jwt_identity()
    user = get_user_by_username(username)
    if not user:
        return jsonify(error="User not found"), 400
    if current_user_id != user.id:
        return jsonify(error="Unauthorized"), 403
    data = request.json
    user = change_password(user.id, data['old_password'], data['new_password'])
    if not user:
        return jsonify(error="Invaild old password"), 400
    return jsonify(message="Password changed successfully"), 200


@api_bp.route('/<string:type>/c', methods=['GET'])
@jwt_required()
def get_categories_route(type):
    user_id = get_jwt_identity()
    categories = search_categories(user_id, type, '')
    categories = [dict(c) for c in categories]
    return jsonify(categories), 200

@api_bp.route('/<string:type>/c', methods=['POST'])
@jwt_required()
def create_category_route(type):
    user_id = get_jwt_identity()
    data = request.json
    category = create_category(user_id, type, data['category_name'])
    if category:
        return jsonify(dict(category)), 201
    return jsonify(error="Failed to create category"), 400

@api_bp.route('/<string:type>/c<int:category_id>', methods=['GET'])
@jwt_required()
def get_category_route(type, category_id):
    user_id = get_jwt_identity()
    category = get_category(user_id, category_id, type)
    if category:
        return jsonify(dict(category)), 200
    return jsonify(error="Category not found"), 404

@api_bp.route('/<string:type>/c<int:category_id>', methods=['PUT'])
@jwt_required()
def update_category_route(type, category_id):
    user_id = get_jwt_identity()
    data = request.json
    category = update_category(user_id, category_id, type, data.get('category_name'))
    if category:
        return jsonify(dict(category)), 200
    return jsonify(error="Category not found"), 404

@api_bp.route('/<string:type>/c<int:category_id>', methods=['DELETE'])
@jwt_required()
def delete_category_route(type, category_id):
    user_id = get_jwt_identity()
    if delete_category(user_id, category_id, type):
        return jsonify(message="Category deleted"), 200
    return jsonify(error="Category not found"), 404

@api_bp.route('/<string:type>/c<int:category_id>/clear', methods=['POST'])
@jwt_required()
def clear_category_route(type, category_id):
    user_id = get_jwt_identity()
    category = clear_category(user_id, category_id, type)
    if category:
        return jsonify(message="Category cleared"), 200
    return jsonify(error="Category not found"), 404

@api_bp.route('/<string:type>/c<int:category_id>/m<int:mark_id>', methods=['GET'])
@jwt_required()
def contains_mark_route(type, category_id, mark_id):
    user_id = get_jwt_identity()
    containsMark = contains_mark(user_id, type, category_id, mark_id)
    return jsonify(containsMark=containsMark), 200

@api_bp.route('/<string:type>/c<int:category_id>/m', methods=['POST'])
@jwt_required()
def add_mark_route(type, category_id):
    user_id = get_jwt_identity()
    data = request.json
    category = add_mark_to_category(user_id, category_id, type, data['mark_id'])
    if category:
        return jsonify(dict(category)), 201
    return jsonify(error="Failed to add mark"), 400

@api_bp.route('/<string:type>/c<int:category_id>/m<int:mark_id>', methods=['DELETE'])
@jwt_required()
def remove_mark_route(type, category_id, mark_id):
    user_id = get_jwt_identity()
    category = remove_mark_from_category(user_id, category_id, type, mark_id)
    if category:
        return jsonify(dict(category)), 200
    return jsonify(error="Failed to remove mark"), 400

@api_bp.route('/<string:type>/c<int:category_id>/m', methods=['GET'])
@jwt_required()
def get_marks_route(type, category_id):
    user_id = get_jwt_identity()
    marks = get_marks_from_category_without_pagination(user_id, category_id, type)
    return jsonify(marks), 200


@api_bp.route('/<string:type>/m<int:mark_id>/is_marked', methods=['GET'])
@jwt_required()
def check_if_mark_exists_route(type, mark_id):
    user_id = get_jwt_identity()
    isMarked = is_marked(user_id, type, mark_id)
    return jsonify(isMarked=isMarked), 200

@api_bp.route('/<string:type>/m/is_marked', methods=['POST'])
@jwt_required()
def check_if_marks_exist_route(type):
    user_id = get_jwt_identity()
    data = request.json
    markIds = data['mark_ids']
    isMarked = {}
    for mark_id in markIds:
        isMarked[mark_id] = is_marked(user_id, type, mark_id)
    return jsonify(isMarked=isMarked), 200

@api_bp.route('/<string:type>/m<int:mark_id>/c', methods=['GET'])
@jwt_required()
def get_categories_by_mark_route(type, mark_id):
    user_id = get_jwt_identity()
    categoryIds = get_categories_by_mark(user_id, type, mark_id)
    return jsonify(categoryIds=categoryIds), 200

@api_bp.route('/<string:type>/m/c', methods=['POST'])
@jwt_required()
def get_categories_by_marks_route(type):
    user_id = get_jwt_identity()
    data = request.json
    markIds = data['mark_ids']
    categoryIds = {}
    for mark_id in markIds:
        categoryIds[mark_id] = get_categories_by_mark(user_id, type, mark_id)
    return jsonify(categoryIds=categoryIds), 200