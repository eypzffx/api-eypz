# app/image_search.py
from flask import Blueprint, request, jsonify
from google_images_search import GoogleImagesSearch

image_search_bp = Blueprint('image_search', __name__)

# Your Google Custom Search JSON API and Custom Search Engine (CSE) ID
GCS_DEVELOPER_KEY = 'AIzaSyD0PmNECLTDPbMm--LMMNEw_mf1GJbXchU'
GCS_CX = 'd567a5ff5da3a47b3'  # Your actual CSE ID

gis = GoogleImagesSearch(GCS_DEVELOPER_KEY, GCS_CX)

@image_search_bp.route('/img', methods=['GET'])
def get_images():
    query = request.args.get('q')
    if not query:
        return jsonify({"error": "Query parameter 'q' is required"}), 400

    query_parts = query.split()
    if len(query_parts) < 1:
        return jsonify({"error": "Query should include a search term"}), 400

    # Default number of images to show
    default_num_images = 3

    if query_parts[-1].isdigit():
        search_term = " ".join(query_parts[:-1])
        num_images = int(query_parts[-1])
    else:
        search_term = " ".join(query_parts)
        num_images = default_num_images

    search_params = {
        'q': search_term,
        'num': num_images,
        'safe': 'off'
    }

    gis.search(search_params=search_params)
    image_urls = [image.url for image in gis.results()]

    return jsonify({"images": image_urls})
