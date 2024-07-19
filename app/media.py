from flask import Blueprint, send_from_directory, jsonify
import os
import random
import json

media_bp = Blueprint('media', __name__)

# Define directories for static files
VIDEO_DIRECTORY = os.path.join(os.getcwd(), 'videos', 'naruto')
IMAGE_DIRECTORY_IMAGE = os.path.join(os.getcwd(), 'images', 'image')
IMAGE_DIRECTORY_CAT = os.path.join(os.getcwd(), 'images', 'cat')
IMAGE_DIRECTORY_TSUNADE = os.path.join(os.getcwd(), 'images', 'tsunade')
IMAGE_DIRECTORY_ANIMEB = os.path.join(os.getcwd(), 'images', 'anime-b')
IMAGE_DIRECTORY_ANIMEG = os.path.join(os.getcwd(), 'images', 'anime-g')
NSFW_WAIFU_FILE = os.path.join(os.getcwd(), 'nsfw', 'waifu.json')
NSFW_NEKO_FILE = os.path.join(os.getcwd(), 'nsfw', 'neko.json')
CAT_FACT_FILE = os.path.join(os.getcwd(), 'chat', 'cat_fact.json')
DETAILS_FILE = os.path.join(os.getcwd(), 'chat', 'details.json')

# Load static files
video_files = os.listdir(VIDEO_DIRECTORY) if os.path.exists(VIDEO_DIRECTORY) else []
image_files_image = os.listdir(IMAGE_DIRECTORY_IMAGE) if os.path.exists(IMAGE_DIRECTORY_IMAGE) else []
image_files_cat = os.listdir(IMAGE_DIRECTORY_CAT) if os.path.exists(IMAGE_DIRECTORY_CAT) else []
image_files_tsunade = os.listdir(IMAGE_DIRECTORY_TSUNADE) if os.path.exists(IMAGE_DIRECTORY_TSUNADE) else []
image_files_animeb = os.listdir(IMAGE_DIRECTORY_ANIMEB) if os.path.exists(IMAGE_DIRECTORY_ANIMEB) else []
image_files_animeg = os.listdir(IMAGE_DIRECTORY_ANIMEG) if os.path.exists(IMAGE_DIRECTORY_ANIMEG) else []

# Load cat facts
def load_cat_facts():
    if os.path.exists(CAT_FACT_FILE):
        with open(CAT_FACT_FILE, 'r') as f:
            cat_facts = json.load(f)
        return cat_facts.get('facts', [])
    return []

CAT_FACTS = load_cat_facts()

# Load details
def load_details():
    if os.path.exists(DETAILS_FILE):
        with open(DETAILS_FILE, 'r') as f:
            details = json.load(f)
        return details
    return {}

DETAILS = load_details()

# Route to serve random media and facts
@media_bp.route('/naruto', methods=['GET'])
def serve_random_naruto_video():
    try:
        if not video_files:
            return "No Naruto videos found", 404
        random_video = random.choice(video_files)
        return send_from_directory(VIDEO_DIRECTORY, random_video)
    except Exception as e:
        return str(e), 500

@media_bp.route('/image', methods=['GET'])
def serve_random_image_image():
    try:
        if not image_files_image:
            return "No images found in 'image' directory", 404
        random_image = random.choice(image_files_image)
        return send_from_directory(IMAGE_DIRECTORY_IMAGE, random_image)
    except Exception as e:
        return str(e), 500

@media_bp.route('/anime-b', methods=['GET'])
def serve_random_image_animeb():
    try:
        if not image_files_animeb:
            return "No images found in 'anime-b' directory", 404
        random_image = random.choice(image_files_animeb)
        return send_from_directory(IMAGE_DIRECTORY_ANIMEB, random_image)
    except Exception as e:
        return str(e), 500

@media_bp.route('/anime-g', methods=['GET'])
def serve_random_image_animeg():
    try:
        if not image_files_animeg:
            return "No images found in 'anime-g' directory", 404
        random_image = random.choice(image_files_animeg)
        return send_from_directory(IMAGE_DIRECTORY_ANIMEG, random_image)
    except Exception as e:
        return str(e), 500

@media_bp.route('/cat', methods=['GET'])
def serve_random_image_cat():
    try:
        if not image_files_cat:
            return "No images found in 'cat' directory", 404
        random_image = random.choice(image_files_cat)
        return send_from_directory(IMAGE_DIRECTORY_CAT, random_image)
    except Exception as e:
        return str(e), 500

@media_bp.route('/tsunade', methods=['GET'])
def serve_random_image_tsunade():
    try:
        if not image_files_tsunade:
            return "No images found in 'tsunade' directory", 404
        random_image = random.choice(image_files_tsunade)
        return send_from_directory(IMAGE_DIRECTORY_TSUNADE, random_image)
    except Exception as e:
        return str(e), 500

@media_bp.route('/cat-fact', methods=['GET'])
def get_random_cat_fact():
    try:
        if not CAT_FACTS:
            return "No cat facts found", 404
        random_fact = random.choice(CAT_FACTS)
        return jsonify({"fact": random_fact})
    except Exception as e:
        return str(e), 500
