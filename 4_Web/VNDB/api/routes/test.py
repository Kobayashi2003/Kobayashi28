import requests
from flask import Blueprint, jsonify, request, render_template_string, current_app
import time

test_bp = Blueprint('test', __name__, url_prefix='/')

@test_bp.route('/', methods=['GET'])
def test_search():
    return render_template_string(form_template)

form_template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Visual Novel Search</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
        }
        .search-modal {
            display: none;
            position: fixed;
            z-index: 1;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            overflow: auto;
            background-color: rgba(0,0,0,0.4);
        }
        .search-content {
            background-color: #fefefe;
            margin: 15% auto;
            padding: 20px;
            border: 1px solid #888;
            width: 80%;
            max-width: 600px;
        }
        .search-tabs {
            display: flex;
            margin-bottom: 20px;
        }
        .search-tab {
            flex: 1;
            padding: 10px;
            border: none;
            background-color: #f1f1f1;
            cursor: pointer;
        }
        .search-tab.active {
            background-color: #ccc;
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
            box-sizing: border-box;
        }
        .search-button {
            background-color: #4CAF50;
            color: white;
            padding: 10px 15px;
            border: none;
            cursor: pointer;
        }
        .close-button {
            color: #aaa;
            float: right;
            font-size: 28px;
            font-weight: bold;
            cursor: pointer;
        }
        .more-options-button {
            background-color: #008CBA;
            color: white;
            padding: 10px 15px;
            border: none;
            cursor: pointer;
        }
        .more-options-content {
            display: none;
        }
        .checkbox-group {
            margin-bottom: 10px;
        }
    </style>
</head>
<body>
    <button id="openSearch">Open Search</button>

    <div id="searchModal" class="search-modal">
        <div class="search-content">
            <h2>Search Visual Novels</h2>
            <div class="search-tabs">
                <button id="localSearchTab" class="search-tab active">Local Search</button>
                <button id="vndbSearchTab" class="search-tab">VNDB Search</button>
            </div>
            <div id="localSearchForm" class="search-form active">
                <form method="get" action="/api/search" class="search-form-local">
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
                    <button type="submit" class="search-button">Search Local</button>
                </form>
            </div>
            <div id="vndbSearchForm" class="search-form">
                <form method="get" action="/api/search" class="search-form-vndb">
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
                    <div class="form-group">
                        <button type="button" id="vndbMoreOptions" class="more-options-button">More Options</button>
                    </div>
                    <div id="vndbMoreOptionsContent" class="more-options-content">
                        <div class="form-group">
                            <label for="vndbReleasedDate">Released Date</label>
                            <input type="text" id="vndbReleasedDate" name="vndbReleasedDate" placeholder="Format: ['<' | '>' | '=' | '<=' | '>=' ] YYYY-MM-DD , ...">
                        </div>
                        <div class="form-group">
                            <label for="vndbLength">Length</label>
                            <select id="vndbLength" name="vndbLength">
                                <option value="">Any</option>
                                <option value="1">Very Short</option>
                                <option value="2">Short</option>
                                <option value="3">Medium</option>
                                <option value="4">Long</option>
                                <option value="5">Very Long</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label for="vndbDevStatus">Development Status</label>
                            <select id="vndbDevStatus" name="vndbDevStatus">
                                <option value="">Any</option>
                                <option value="0">Finished</option>
                                <option value="1">In development</option>
                                <option value="2">Cancelled</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label>Additional Filters</label>
                            <div class="checkbox-group">
                                <input type="checkbox" id="vndbHasDescription" name="vndbHasDescription">
                                <label for="vndbHasDescription">Has Description</label>
                            </div>
                            <div class="checkbox-group">
                                <input type="checkbox" id="vndbHasAnime" name="vndbHasAnime">
                                <label for="vndbHasAnime">Has Anime</label>
                            </div>
                            <div class="checkbox-group">
                                <input type="checkbox" id="vndbHasScreenshot" name="vndbHasScreenshot">
                                <label for="vndbHasScreenshot">Has Screenshot</label>
                            </div>
                            <div class="checkbox-group">
                                <input type="checkbox" id="vndbHasReview" name="vndbHasReview">
                                <label for="vndbHasReview">Has Review</label>
                            </div>
                        </div>
                    </div>
                    <button type="submit" class="search-button">Search VNDB</button>
                </form>
            </div>
            <button id="closeSearch" class="close-button">&times;</button>
        </div>
    </div>

    <script>
        document.addEventListener('DOMContentLoaded', function() {
            const modal = document.getElementById('searchModal');
            const openBtn = document.getElementById('openSearch');
            const closeBtn = document.getElementById('closeSearch');
            const localTab = document.getElementById('localSearchTab');
            const vndbTab = document.getElementById('vndbSearchTab');
            const localForm = document.getElementById('localSearchForm');
            const vndbForm = document.getElementById('vndbSearchForm');
            const moreOptionsBtn = document.getElementById('vndbMoreOptions');
            const moreOptionsContent = document.getElementById('vndbMoreOptionsContent');

            openBtn.onclick = function() {
                modal.style.display = 'block';
            }

            closeBtn.onclick = function() {
                modal.style.display = 'none';
            }

            window.onclick = function(event) {
                if (event.target == modal) {
                    modal.style.display = 'none';
                }
            }

            localTab.onclick = function() {
                localTab.classList.add('active');
                vndbTab.classList.remove('active');
                localForm.classList.add('active');
                vndbForm.classList.remove('active');
            }

            vndbTab.onclick = function() {
                vndbTab.classList.add('active');
                localTab.classList.remove('active');
                vndbForm.classList.add('active');
                localForm.classList.remove('active');
            }

            moreOptionsBtn.onclick = function() {
                moreOptionsContent.style.display = moreOptionsContent.style.display === 'none' ? 'block' : 'none';
            }
        });
    </script>
</body>
</html>
'''
