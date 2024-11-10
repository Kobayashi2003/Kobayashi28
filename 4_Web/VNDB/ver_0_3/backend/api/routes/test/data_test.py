from flask import Blueprint, jsonify, request, render_template, current_app
import requests

data_test_routes = Blueprint('data_test', __name__)

@data_test_routes.route('/data', methods=['GET', 'POST'])
def test_data():
    if request.method == 'POST':
        return handle_data_request()
    return render_template('test_data.html')

def handle_data_request():
    data_type = request.form.get('dataType')
    id = request.form.get('id')
    data_size = request.form.get('dataSize', 'small')

    try:
        port = current_app.config['APP_PORT']
        api_url = f'http://localhost:{port}/api/data/{data_type}/{id}/{data_size}'
        api_response = requests.get(api_url)
        api_response.raise_for_status()
        task_id = api_response.json()['task_id']
        return jsonify({'task_id': task_id})
    except Exception as e:
        return jsonify({"error": str(e)}), 400