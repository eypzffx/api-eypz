# app/shorten.py
from flask import Blueprint, jsonify, request, redirect
import pyshorteners
import random
import string

shorten_bp = Blueprint('shorten', __name__)
s = pyshorteners.Shortener()

# Dictionary to store custom short URLs
custom_urls = {}

def generate_random_string(length=8):
    """Generate a random string of specified length."""
    letters = string.ascii_lowercase + string.ascii_uppercase + string.digits
    return ''.join(random.choice(letters) for _ in range(length))

@shorten_bp.route('/shorten', methods=['POST', 'GET'])
def shorten_url():
    long_url = None

    if request.method == 'POST':
        # Handle JSON request body
        long_url = request.json.get('url')
    elif request.method == 'GET':
        # Handle URL query parameter
        long_url = request.args.get('url')

    if not long_url:
        return jsonify({'error': 'Missing URL parameter'}), 400

    try:
        # Generate a random short code
        short_code = generate_random_string()
        
        # Store the mapping of short code to long URL
        custom_urls[short_code] = long_url
        
        # Construct the custom short URL
        short_url = f"{request.host_url}{short_code}"
        
        return jsonify({'short_url': short_url}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@shorten_bp.route('/<short_code>', methods=['GET'])
def redirect_to_original(short_code):
    if short_code in custom_urls:
        long_url = custom_urls[short_code]
        return redirect(long_url, code=302)
    else:
        return jsonify({'error': 'Short URL not found'}), 404
