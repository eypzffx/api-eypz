# app/instagram.py
from flask import Blueprint, jsonify, request
from stalking.insta import get_instagram_profile

instagram_bp = Blueprint('instagram', __name__)

@instagram_bp.route('/instagram', methods=['GET'])
def get_insta_profile():
    username = request.args.get('username')
    if not username:
        return jsonify({'error': 'Missing username parameter'}), 400

    profile_info, error = get_instagram_profile(username)
    if error:
        return jsonify({'error': error}), 500

    return jsonify(profile_info)
