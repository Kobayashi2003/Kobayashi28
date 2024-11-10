from flask import Blueprint, jsonify, request, render_template, current_app
import requests
from api.search.local.search import search as local_search
from api.db.crud import create, update, delete, get, get_all

test_bp = Blueprint('test', __name__, url_prefix='/test')

@test_bp.route('/')
def test_index():
    return render_template('test_index.html')

@test_bp.route('/search/remote', methods=['GET', 'POST'])
def test_remote_search():
    if request.method == 'POST':
        return handle_search('remote')
    return render_template('test_search.html', search_type='remote')

@test_bp.route('/search/local', methods=['GET', 'POST'])
def test_local_search():
    if request.method == 'POST':
        return handle_search('local')
    return render_template('test_search.html', search_type='local')

def handle_search(search_from):
    search_type = request.form.get('searchType', 'vn')
    response_size = request.form.get('responseSize', 'small')
    params = {k: v for k, v in request.form.items() if v and k not in ['searchType', 'responseSize']}

    try:
        port = current_app.config['APP_PORT']
        api_url = f'http://localhost:{port}/api/search'
        api_response = requests.post(api_url, json={
            'searchFrom': search_from,
            'searchType': search_type,
            'responseSize': response_size,
            **params
        })
        api_response.raise_for_status()
        task_id = api_response.json()['task_id']
        return jsonify({'task_id': task_id})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@test_bp.route('/crud', methods=['GET', 'POST'])
def test_crud():
    if request.method == 'POST':
        return handle_crud_operation()
    return render_template('test_crud.html')

def to_dict(obj):
    if hasattr(obj, 'to_dict'):
        return obj.to_dict()
    return {k: v for k, v in vars(obj).items() if not k.startswith('_')}

def handle_crud_operation():
    operation = request.form.get('operation')
    model_type = request.form.get('modelType')
    id = request.form.get('id')
    data = {k: v for k, v in request.form.items() if k not in ['operation', 'modelType', 'id']}

    try:
        if operation == 'create':
            item = create(model_type, id, data)
            return jsonify({"message": f"Created {model_type} with ID: {item.id}"})
        elif operation == 'read':
            if id:
                item = get(model_type, id)
                if item:
                    return jsonify(to_dict(item))
                return jsonify({"error": "Item not found"}), 404
            else:
                items = get_all(model_type)
                return jsonify([to_dict(item) for item in items])
        elif operation == 'update':
            item = update(model_type, id, data)
            if item:
                return jsonify({"message": f"Updated {model_type} with ID: {id}"})
            return jsonify({"error": "Item not found"}), 404
        elif operation == 'delete':
            success = delete(model_type, id)
            if success:
                return jsonify({"message": f"Deleted {model_type} with ID: {id}"})
            return jsonify({"error": "Item not found"}), 404
        else:
            return jsonify({"error": "Invalid operation"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400