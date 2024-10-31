from vndb.db import connect_db

from flask import Blueprint, current_app, jsonify

import os
import shutil

def delete_vn(id: str) -> bool:

    vn_images_path = os.path.join(current_app.config['STATIC_FOLDER'], 'images', id)

    if os.path.exists(vn_images_path):
        shutil.rmtree(vn_images_path)

    conn = connect_db()
    with conn.cursor() as curs:
        curs.execute("DELETE FROM vn WHERE id = %s", (id,))
        conn.commit()

    return True


delete_bp = Blueprint('delete', __name__, 
                      url_prefix='/delete',
                      template_folder='templates',
                      static_folder='static')

@delete_bp.route('/<id>', methods=['POST'])
def delete(id):
    try:
        success = delete_vn(id=id)
        if not success:
            return jsonify({"status": "error", "message": "VN delete failed"}), 404
        return jsonify({"status": "success", "message": "VN deleted successfully"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
