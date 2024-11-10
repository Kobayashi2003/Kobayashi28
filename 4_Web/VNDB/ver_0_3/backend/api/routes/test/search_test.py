from flask import Blueprint, jsonify, request, render_template, current_app
import requests

search_test_routes = Blueprint('search_test', __name__)

@search_test_routes.route('/search/remote', methods=['GET', 'POST'])
def test_remote_search():
    if request.method == 'POST':
        return handle_search('remote')
    return render_template('test_search.html', search_type='remote')

@search_test_routes.route('/search/local', methods=['GET', 'POST'])
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