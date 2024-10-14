from vndb.db import connect_db
from vndb.search import search_vndb, generate_fields, generate_filters

from flask import current_app, url_for, Blueprint, jsonify, redirect
from werkzeug.utils import secure_filename

import os
import json
import requests
from concurrent.futures import ThreadPoolExecutor

def download_image(image_url: str, path: str):

    if os.path.exists(os.path.join(path, os.path.basename(image_url))):
        return True

    response = requests.get(image_url, headers={ 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36' }, timeout=10)
    if response.status_code == 200:
        content_image = response.content
        with open(os.path.join(path, os.path.basename(image_url)), 'wb') as f:
            f.write(content_image)
        return True

    return False

def download_vn(id: str) -> bool:

    static_path = current_app.config['STATIC_FOLDER']
    download_path = os.path.join(static_path, 'images', id)
    os.makedirs(download_path, exist_ok=True)

    conn = connect_db()
    with conn.cursor() as curs:
        curs.execute("SELECT data FROM vn WHERE id = %s", (id,))
        result = curs.fetchone()
        if not result:
            fields = generate_fields()
            filter = generate_filters(id=id)
            result = search_vndb(fields=fields, filters=filter)
            result = result['results'] if result else []
            if not result:
                return False
            curs.execute("INSERT INTO vn (id, data) VALUES (%s, %s)", (id, json.dumps(result[0])))
        data = result[0]

        images = []

        if 'url' in data['image'] and data['image']['url']:
            images.append(data['image']['url'])
            data['image']['local'] = url_for('static', filename=os.path.join('images', id, os.path.basename(data['image']['url'])).replace('\\', '/'))
            data['image']['local_thumbnail'] = url_for('static', filename=os.path.join('images', id, os.path.basename(data['image']['thumbnail'])).replace('\\', '/'))
        for screenshot in data['screenshots']:
            if 'url' in screenshot and screenshot['url']:
                images.append(screenshot['url'])
                screenshot['local'] = url_for('static', filename=os.path.join('images', id, os.path.basename(screenshot['url'])).replace('\\', '/'))
            if 'thumbnail' in screenshot and screenshot['thumbnail']:
                images.append(screenshot['thumbnail'])
                screenshot['local_thumbnail'] = url_for('static', filename=os.path.join('images', id, os.path.basename(screenshot['thumbnail'])).replace('\\', '/'))
        for va in data['va']:
            if 'character' in va and va['character'] and 'url' in va['character']['image'] and va['character']['image']['url']:
                images.append(va['character']['image']['url'])
                va['character']['image']['local'] = url_for('static', filename=os.path.join('images', id, os.path.basename(va['character']['image']['url'])).replace('\\', '/'))
        curs.execute("UPDATE vn SET data = %s WHERE id = %s", (json.dumps(data), id))
        curs.execute("UPDATE vn SET downloaded = true WHERE id = %s", (id,))
        conn.commit()

    with ThreadPoolExecutor(max_workers=10) as executor:
        for image in images:
            executor.submit(download_image, image, download_path)

    return True

download_bp = Blueprint('download', __name__, url_prefix='/download')

@download_bp.route('/<id>', methods=['POST'])
def download(id):
    try:
        success = download_vn(id=id)
        if not success:
            return jsonify({"status": "error", "message": "VN download failed"}), 404
        return jsonify({"status": "success", "message": "VN downloaded successfully"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
