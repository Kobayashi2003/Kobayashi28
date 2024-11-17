from flask import Blueprint, jsonify, request
from app.database import Bookmark
from app import db
import json

bp = Blueprint('main', __name__)

@bp.route('/api/bookmarks', methods=['POST'])
def create_bookmark():
    data = request.json or {}
    new_bookmark = Bookmark(
        name=data.get('name', ''),
        host=data.get('host', ''),
        route=data.get('route', ''),
        method=data.get('method', 'GET'),
        params=json.dumps(data.get('params', {})),
        body=data.get('body', '')
    )
    db.session.add(new_bookmark)
    db.session.commit()
    return jsonify({"message": "Bookmark added successfully", "id": new_bookmark.id}), 201

@bp.route('/api/bookmarks', methods=['GET'])
def list_bookmarks():
    bookmarks = Bookmark.query.order_by(Bookmark.created_at.desc()).all()
    return jsonify([bookmark.to_dict() for bookmark in bookmarks])

@bp.route('/api/bookmarks/<int:id>', methods=['DELETE'])
def delete_bookmark(id):
    bookmark = Bookmark.query.get_or_404(id)
    db.session.delete(bookmark)
    db.session.commit()
    return jsonify({"message": "Bookmark deleted successfully"}), 200

# Add a catch-all route for undefined API endpoints
@bp.route('/api/<path:undefined_route>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def undefined_api_route(undefined_route):
    return jsonify({
        "error": "Undefined API route",
        "method": request.method,
        "route": f"/api/{undefined_route}",
    }), 404