from flask import jsonify, current_app
import requests

def make_api_request(method, endpoint, data=None):
    try:
        port = current_app.config['APP_PORT']
        api_url = f'http://localhost:{port}/api/{endpoint}'
        
        if method == 'GET':
            response = requests.get(api_url)
        elif method == 'POST':
            response = requests.post(api_url, json=data)
        elif method == 'DELETE':
            response = requests.delete(api_url)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")
        
        response.raise_for_status()
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 400

def get_task_status(task_type, task_id):
    return make_api_request('GET', f'{task_type}/status/{task_id}')