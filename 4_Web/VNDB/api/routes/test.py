import requests
from flask import Blueprint, jsonify, request, render_template_string, current_app
import time

test_bp = Blueprint('test', __name__, url_prefix='/')

@test_bp.route('/', methods=['GET'])
def test_search():
    return render_template_string(template)

template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Visual Novel Search</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        h1 {
            text-align: center;
        }
        .search-container {
            background-color: #f4f4f4;
            padding: 20px;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        .search-tabs {
            display: flex;
            margin-bottom: 20px;
        }
        .search-tab {
            flex: 1;
            padding: 10px;
            text-align: center;
            background-color: #ddd;
            cursor: pointer;
        }
        .search-tab.active {
            background-color: #f4f4f4;
        }
        .search-form {
            display: none;
        }
        .search-form.active {
            display: block;
        }
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
        }
        input[type="text"], select {
            width: 100%;
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
        }
        button {
            display: block;
            width: 100%;
            padding: 10px;
            background-color: #5cb85c;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        button:hover {
            background-color: #4cae4c;
        }
        #searchResults {
            background-color: #f4f4f4;
            padding: 20px;
            border-radius: 5px;
            white-space: pre-wrap;
            overflow-wrap: break-word;
        }
    </style>
</head>
<body>
    <h1>Visual Novel Search</h1>
    <div class="search-container">
        <div class="search-tabs">
            <div class="search-tab active" data-tab="local">Local Search</div>
            <div class="search-tab" data-tab="vndb">VNDB Search</div>
        </div>
        <form id="localSearchForm" class="search-form active">
            <input type="hidden" name="searchType" value="local">
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
            <input type="hidden" name="searchType" value="vndb">
            <div class="form-group">
                <label for="vndbQuery">Query</label>
                <input type="text" id="vndbQuery" name="vndbQuery" placeholder="Enter search query">
            </div>
            <div class="form-group">
                <label for="vndbDevelopers">Developers</label>
                <input type="text" id="vndbDevelopers" name="vndbDevelopers" placeholder="Enter developers. Separated by commas">
            </div>
            <div class="form-group">
                <label for="vndbStaffs">Staffs</label>
                <input type="text" id="vndbStaffs" name="vndbStaffs" placeholder="Enter staffs. Separated by commas">
            </div>
            <div class="form-group">
                <label for="vndbCharacters">Characters</label>
                <input type="text" id="vndbCharacters" name="vndbCharacters" placeholder="Enter characters. Separated by commas">
            </div>
            <button type="submit">Search VNDB</button>
        </form>
    </div>
    <div id="searchResults"></div>

    <script>
        document.addEventListener('DOMContentLoaded', function() {
            const tabs = document.querySelectorAll('.search-tab');
            const forms = document.querySelectorAll('.search-form');

            tabs.forEach(tab => {
                tab.addEventListener('click', () => {
                    tabs.forEach(t => t.classList.remove('active'));
                    forms.forEach(f => f.classList.remove('active'));
                    tab.classList.add('active');
                    document.querySelector(`#${tab.dataset.tab}SearchForm`).classList.add('active');
                });
            });

            const localForm = document.getElementById('localSearchForm');
            const vndbForm = document.getElementById('vndbSearchForm');
            const resultsDiv = document.getElementById('searchResults');

            [localForm, vndbForm].forEach(form => {
                form.addEventListener('submit', async (e) => {
                    e.preventDefault();
                    resultsDiv.textContent = 'Searching...';
                    const formData = new FormData(form);
                    try {
                        const response = await fetch(`/api/search?${new URLSearchParams(formData)}`, {
                            method: 'GET'
                        });
                        const data = await response.json();
                        if (data.task_id) {
                            await pollForResults(data.task_id);
                        } else {
                            displayResults(data);
                        }
                    } catch (error) {
                        resultsDiv.textContent = `Error: ${error.message}`;
                    }
                });
            });

            async function pollForResults(taskId) {
                const maxAttempts = 30;
                const interval = 1000; // 1 second
                for (let attempt = 0; attempt < maxAttempts; attempt++) {
                    const response = await fetch(`/api/search/status/${taskId}`);
                    const data = await response.json();
                    if (data.state === 'SUCCESS') {
                        displayResults(data.result);
                        return;
                    } else if (data.state === 'FAILURE') {
                        resultsDiv.textContent = 'Search failed';
                        return;
                    }
                    await new Promise(resolve => setTimeout(resolve, interval));
                }
                resultsDiv.textContent = 'Search timed out';
            }

            function displayResults(results) {
                resultsDiv.textContent = JSON.stringify(results, null, 2);
            }
        });
    </script>
</body>
</html>
'''