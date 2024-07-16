from flask import Blueprint, jsonify, redirect, request
import pyshorteners
import random
import string

shorten_bp = Blueprint('shorten_bp', __name__)

s = pyshorteners.Shortener()

# Dictionary to store custom short URLs
custom_urls = {}

def generate_random_string(length=8):
    """Generate a random string of specified length."""
    letters = string.ascii_lowercase + string.ascii_uppercase + string.digits
    return ''.join(random.choice(letters) for _ in range(length))

# Endpoint to shorten a URL with custom short URL
@shorten_bp.route('/shorten', methods=['POST'])
def shorten_url():
    long_url = request.json.get('url')

    if not long_url:
        return jsonify({'error': 'Missing URL parameter'}), 400

    try:
        short_code = generate_random_string()
        custom_urls[short_code] = long_url
        short_url = f"{request.host_url}{short_code}"
        return jsonify({'short_url': short_url}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Redirect to the original URL using the custom short URL
@shorten_bp.route('/<short_code>', methods=['GET'])
def redirect_to_original(short_code):
    if short_code in custom_urls:
        long_url = custom_urls[short_code]
        return redirect(long_url, code=302)
    else:
        return jsonify({'error': 'Short URL not found'}), 404
