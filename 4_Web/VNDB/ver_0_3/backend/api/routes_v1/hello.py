from flask import Blueprint, jsonify

hello_bp = Blueprint('hello', __name__, url_prefix='/hello')

@hello_bp.route('/', methods=['GET'])
def hello_world():
    return jsonify({"message": "Hello, KOBAYASHI!"})