from flask import Blueprint, request, render_template
from .utils import make_api_request, get_task_status

search_test_routes = Blueprint('search_test', __name__)

@search_test_routes.route('/search/<search_from>', methods=['GET', 'POST'])
def test_search(search_from):
    if request.method == 'POST':
        search_type = request.form.get('searchType', 'vn')
        response_size = request.form.get('responseSize', 'small')
        params = {k: v for k, v in request.form.items() if v and k not in ['searchType', 'responseSize']}
        data = {
            'searchFrom': search_from,
            'searchType': search_type,
            'responseSize': response_size,
            **params
        }
        return make_api_request('POST', 'search', data)
    return render_template('test_search.html', search_type=search_from)

@search_test_routes.route('/search/status/<task_id>', methods=['GET'])
def search_status(task_id):
    return get_task_status('search', task_id)