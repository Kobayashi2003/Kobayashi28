from flask import Blueprint, jsonify, request, render_template, current_app
import requests

update_test_routes = Blueprint('update_test', __name__)

@update_test_routes.route('/update', methods=['GET', 'POST'])
def test_update():
    if request.method == 'POST':
        return handle_update_request()
    return render_template('test_update.html')

def handle_update_request():
    update_type = request.form.get('updateType')
    id = request.form.get('id')

    try:
        port = current_app.config['APP_PORT']
        api_url = f'http://localhost:{port}/api/update/{update_type}/{id}'
        api_response = requests.post(api_url)
        api_response.raise_for_status()
        task_id = api_response.json()['task_id']
        return jsonify({'task_id': task_id})
    except Exception as e:
        return jsonify({"error": str(e)}), 400