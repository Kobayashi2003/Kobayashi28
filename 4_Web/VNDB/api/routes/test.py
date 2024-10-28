import requests
from flask import Blueprint, jsonify, request, render_template_string, current_app
import time
import json

test_bp = Blueprint('test', __name__, url_prefix='/')

@test_bp.route('/', methods=['GET', 'POST'])
def test_operations():
    if request.method == 'POST':
        operation = request.form.get('operation')
        if operation == 'search':
            return handle_search()
        elif operation == 'create':
            return handle_create()
        elif operation == 'update':
            return handle_update()
        elif operation == 'delete':
            return handle_delete()
        else:
            return jsonify({"error": "Invalid operation"}), 400
    return render_template_string(template)

def handle_search():
    search_type = request.form.get('searchType')
    
    search_url = f"{request.url_root}api/search"
    params = {k: v for k, v in request.form.items() if v}
    
    response = requests.get(search_url, params=params)
    
    if response.status_code == 202:
        task_id = response.json()['task_id']
        return poll_for_results(task_id, 'search')
    else:
        return jsonify({"error": "Search request failed"}), response.status_code

def handle_create():
    vn_id = request.form.get('id')
    vn_data = request.form.get('data')
    
    try:
        vn_data_json = json.loads(vn_data)
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON data"}), 400
    
    create_url = f"{request.url_root}api/create"
    response = requests.post(create_url, json={"id": vn_id, "data": vn_data_json})
    
    if response.status_code == 202:
        task_id = response.json()['task_id']
        return poll_for_results(task_id, 'create')
    else:
        return jsonify({"error": "Create request failed"}), response.status_code

def handle_update():
    vn_id = request.form.get('id')
    vn_data = request.form.get('data')
    downloaded = request.form.get('downloaded')
    
    update_data = {"id": vn_id}
    if vn_data:
        try:
            update_data["data"] = json.loads(vn_data)
        except json.JSONDecodeError:
            return jsonify({"error": "Invalid JSON data"}), 400
    if downloaded:
        update_data["downloaded"] = downloaded.lower() == 'true'
    
    update_url = f"{request.url_root}api/update"
    response = requests.post(update_url, json=update_data)
    
    if response.status_code == 202:
        task_id = response.json()['task_id']
        return poll_for_results(task_id, 'update')
    else:
        return jsonify({"error": "Update request failed"}), response.status_code

def handle_delete():
    vn_id = request.form.get('id')
    
    delete_url = f"{request.url_root}api/delete"
    response = requests.post(delete_url, json={"id": vn_id})
    
    if response.status_code == 202:
        task_id = response.json()['task_id']
        return poll_for_results(task_id, 'delete')
    else:
        return jsonify({"error": "Delete request failed"}), response.status_code

def poll_for_results(task_id, operation):
    max_retries = 30
    for _ in range(max_retries):
        status_url = f"{request.url_root}api/{operation}/status/{task_id}"
        status_response = requests.get(status_url)
        status_data = status_response.json()
        
        if status_data['state'] == 'SUCCESS':
            return jsonify(status_data['result'])
        elif status_data['state'] == 'FAILURE':
            return jsonify({"error": f"{operation.capitalize()} failed"}), 500
        
        time.sleep(1)
    
    return jsonify({"error": f"{operation.capitalize()} timed out"}), 504

template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Visual Novel Database Operations</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        h1, h2 {
            text-align: center;
        }
        .operation-tabs {
            display: flex;
            justify-content: space-around;
            margin-bottom: 20px;
        }
        .operation-tab {
            padding: 10px 20px;
            cursor: pointer;
            background-color: #f0f0f0;
            border: 1px solid #ddd;
            border-radius: 5px;
        }
        .operation-tab.active {
            background-color: #007bff;
            color: white;
        }
        .operation-form {
            display: none;
            background-color: #f9f9f9;
            padding: 20px;
            border-radius: 5px;
        }
        .operation-form.active {
            display: block;
        }
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
        }
        input[type="text"], select, textarea {
            width: 100%;
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
            box-sizing: border-box;
        }
        button {
            display: block;
            width: 100%;
            padding: 10px;
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        button:hover {
            background-color: #0056b3;
        }
        #results {
            margin-top: 20px;
            background-color: #f0f0f0;
            padding: 20px;
            border-radius: 5px;
            white-space: pre-wrap;
            overflow-wrap: break-word;
        }
        .search-tabs {
            display: flex;
            margin-bottom: 20px;
        }
        .search-tab {
            flex: 1;
            padding: 10px;
            text-align: center;
            background-color: #f4f4f4;
            cursor: pointer;
        }
        .search-tab.active {
            background-color: #ddd;
        }
        .search-form {
            display: none;
        }
        .search-form.active {
            display: block;
        }
    </style>
</head>
<body>
    <h1>Visual Novel Database Operations</h1>
    <div class="operation-tabs">
        <div class="operation-tab active" data-operation="search">Search</div>
        <div class="operation-tab" data-operation="create">Create</div>
        <div class="operation-tab" data-operation="update">Update</div>
        <div class="operation-tab" data-operation="delete">Delete</div>
    </div>
    
    <div id="searchForm" class="operation-form active">
        <div class="search-tabs">
            <div class="search-tab active" data-tab="local">Local Search</div>
            <div class="search-tab" data-tab="vndb">VNDB Search</div>
        </div>
        <form id="localSearchForm" class="search-form active">
            <input type="hidden" name="operation" value="search">
            <input type="hidden" name="searchType" value="local">
            <input type="hidden" name="responseSize" value="small">
            <div class="form-group">
                <label for="localTitle">Title</label>
                <input type="text" id="localTitle" name="localTitle" placeholder="Enter title">
            </div>
            <div class="form-group">
                <label for="localDevelopers">Developers</label>
                <input type="text" id="localDevelopers" name="localDevelopers" placeholder="Enter developers">
            </div>
            <div class="form-group">
                <label for="localCharacters">Characters</label>
                <input type="text" id="localCharacters" name="localCharacters" placeholder="Enter characters">
            </div>
            <div class="form-group">
                <label for="localLength">Length</label>
                <select id="localLength" name="localLength">
                    <option value="">Any</option>
                    <option value="1">Very Short</option>
                    <option value="2">Short</option>
                    <option value="3">Medium</option>
                    <option value="4">Long</option>
                    <option value="5">Very Long</option>
                </select>
            </div>
            <button type="submit">Search Local</button>
        </form>
        <form id="vndbSearchForm" class="search-form">
            <input type="hidden" name="operation" value="search">
            <input type="hidden" name="searchType" value="vndb">
            <div class="form-group">
                <label for="vndbQuery">Query</label>
                <input type="text" id="vndbQuery" name="vndbQuery" placeholder="Enter search query">
            </div>
            <div class="form-group">
                <label for="vndbDevelopers">Developers</label>
                <input type="text" id="vndbDevelopers" name="vndbDevelopers" placeholder="Enter developers">
            </div>
            <div class="form-group">
                <label for="vndbStaffs">Staffs</label>
                <input type="text" id="vndbStaffs" name="vndbStaffs" placeholder="Enter staffs">
            </div>
            <div class="form-group">
                <label for="vndbCharacters">Characters</label>
                <input type="text" id="vndbCharacters" name="vndbCharacters" placeholder="Enter characters">
            </div>
            <button type="submit">Search VNDB</button>
        </form>
    </div>
    
    <form id="createForm" class="operation-form">
        <input type="hidden" name="operation" value="create">
        <div class="form-group">
            <label for="createId">VN ID:</label>
            <input type="text" id="createId" name="id" required>
        </div>
        <div class="form-group">
            <label for="createData">VN Data (JSON):</label>
            <textarea id="createData" name="data" required></textarea>
        </div>
        <button type="submit">Create VN</button>
    </form>
    
    <form id="updateForm" class="operation-form">
        <input type="hidden" name="operation" value="update">
        <div class="form-group">
            <label for="updateId">VN ID:</label>
            <input type="text" id="updateId" name="id" required>
        </div>
        <div class="form-group">
            <label for="updateData">VN Data (JSON):</label>
            <textarea id="updateData" name="data"></textarea>
        </div>
        <div class="form-group">
            <label for="updateDownloaded">Downloaded:</label>
            <select id="updateDownloaded" name="downloaded">
                <option value="">No change</option>
                <option value="true">True</option>
                <option value="false">False</option>
            </select>
        </div>
        <button type="submit">Update VN</button>
    </form>
    
    <form id="deleteForm" class="operation-form">
        <input type="hidden" name="operation" value="delete">
        <div class="form-group">
            <label for="deleteId">VN ID:</label>
            <input type="text" id="deleteId" name="id" required>
        </div>
        <button type="submit">Delete VN</button>
    </form>
    
    <div id="results"></div>
    
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            const operationTabs = document.querySelectorAll('.operation-tab');
            const operationForms = document.querySelectorAll('.operation-form');
            const searchTabs = document.querySelectorAll('.search-tab');
            const searchForms = document.querySelectorAll('.search-form');
            const resultsDiv = document.getElementById('results');

            operationTabs.forEach(tab => {
                tab.addEventListener('click', () => {
                    operationTabs.forEach(t => t.classList.remove('active'));
                    operationForms.forEach(f => f.classList.remove('active'));
                    tab.classList.add('active');
                    document.getElementById(`${tab.dataset.operation}Form`).classList.add('active');
                });
            });

            searchTabs.forEach(tab => {
                tab.addEventListener('click', () => {
                    searchTabs.forEach(t => t.classList.remove('active'));
                    searchForms.forEach(f => f.classList.remove('active'));
                    tab.classList.add('active');
                    document.getElementById(`${tab.dataset.tab}SearchForm`).classList.add('active');
                });
            });

            document.querySelectorAll('form').forEach(form => {
                form.addEventListener('submit', async (e) => {
                    e.preventDefault();
                    resultsDiv.textContent = 'Processing...';
                    const formData = new FormData(form);
                    try {
                        const response = await fetch('/', {
                            method: 'POST',
                            body: formData
                        });
                        const data = await response.json();
                        resultsDiv.textContent = JSON.stringify(data, null, 2);
                    } catch (error) {
                        resultsDiv.textContent = `Error: ${error.message}`;
                    }
                });
            });
        });
    </script>
</body>
</html>
'''