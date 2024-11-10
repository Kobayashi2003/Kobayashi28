from flask import Blueprint, jsonify, request, render_template
from api.db.crud import create, update, delete, get, get_all

crud_test_routes = Blueprint('crud_test', __name__)

@crud_test_routes.route('/crud', methods=['GET', 'POST'])
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