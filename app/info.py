from flask import Blueprint, jsonify

info_bp = Blueprint('info', __name__)

@info_bp.route('/info', methods=['GET'])
def get_info():
    return jsonify({"info": "This is your Flask API"})
