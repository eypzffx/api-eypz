from flask import Flask, jsonify, send_from_directory, render_template, request
import os
import random
import json
import requests
from bs4 import BeautifulSoup

# Import the Instagram profile fetching function and YouTube thumbnail fetching function
from stalking.insta import get_instagram_profile
from stalking.youtube import get_youtube_thumbnail

app = Flask(__name__)

# Define directories for static files
VIDEO_DIRECTORY = os.path.join(os.getcwd(), 'videos', 'naruto')
IMAGE_DIRECTORY_IMAGE = os.path.join(os.getcwd(), 'images', 'image')
IMAGE_DIRECTORY_CAT = os.path.join(os.getcwd(), 'images', 'cat')
IMAGE_DIRECTORY_TSUNADE = os.path.join(os.getcwd(), 'images', 'tsunade')
CAT_FACT_FILE = os.path.join(os.getcwd(), 'chat', 'cat_fact.json')
DETAILS_FILE = os.path.join(os.getcwd(), 'chat', 'details.json')

# Load static files
video_files = os.listdir(VIDEO_DIRECTORY)
image_files_image = os.listdir(IMAGE_DIRECTORY_IMAGE)
image_files_cat = os.listdir(IMAGE_DIRECTORY_CAT)
image_files_tsunade = os.listdir(IMAGE_DIRECTORY_TSUNADE)

# Load cat facts
def load_cat_facts():
    with open(CAT_FACT_FILE, 'r') as f:
        cat_facts = json.load(f)
    return cat_facts['facts'] if 'facts' in cat_facts else []

CAT_FACTS = load_cat_facts()

# Load details
def load_details():
    with open(DETAILS_FILE, 'r') as f:
        details = json.load(f)
    return details

DETAILS = load_details()

# Root route to render index.html
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# Routes to serve random media and facts
@app.route('/naruto', methods=['GET'])
def serve_random_naruto_video():
    try:
        random_video = random.choice(video_files)
        return send_from_directory(VIDEO_DIRECTORY, random_video)
    except IndexError:
        return "No Naruto videos found", 404
    except Exception as e:
        return str(e), 500

@app.route('/image', methods=['GET'])
def serve_random_image_image():
    try:
        random_image = random.choice(image_files_image)
        return send_from_directory(IMAGE_DIRECTORY_IMAGE, random_image)
    except IndexError:
        return "No images found in 'image' directory", 404
    except Exception as e:
        return str(e), 500

@app.route('/cat', methods=['GET'])
def serve_random_image_cat():
    try:
        random_image = random.choice(image_files_cat)
        return send_from_directory(IMAGE_DIRECTORY_CAT, random_image)
    except IndexError:
        return "No images found in 'cat' directory", 404
    except Exception as e:
        return str(e), 500

@app.route('/tsunade', methods=['GET'])
def serve_random_image_tsunade():
    try:
        random_image = random.choice(image_files_tsunade)
        return send_from_directory(IMAGE_DIRECTORY_TSUNADE, random_image)
    except IndexError:
        return "No images found in 'tsunade' directory", 404
    except Exception as e:
        return str(e), 500

@app.route('/cat-fact', methods=['GET'])
def get_random_cat_fact():
    try:
        random_fact = random.choice(CAT_FACTS)
        return jsonify({"fact": random_fact})
    except IndexError:
        return "No cat facts found", 404
    except Exception as e:
        return str(e), 500

@app.route('/details/<category>', methods=['GET'])
def get_random_fact(category):
    try:
        if category in DETAILS:
            facts = DETAILS[category]
            random_fact = random.choice(facts)
            return jsonify({"fact": random_fact})
        else:
            return f"No facts found for category '{category}'", 404
    except IndexError:
        return f"No facts found for category '{category}'", 404
    except Exception as e:
        return str(e), 500

@app.route('/download_thumbnail', methods=['GET'])
def download_thumbnail():
    video_url = request.args.get('url')
    if not video_url:
        return jsonify({'error': 'Missing video URL parameter'}), 400
    
    thumbnail_url, error = get_youtube_thumbnail(video_url)
    if error:
        return jsonify({'error': error}), 500
    
    return jsonify({'thumbnail_url': thumbnail_url})

@app.route('/insta', methods=['GET'])
def get_insta_profile():
    username = request.args.get('username')
    if not username:
        return jsonify({'error': 'Missing username parameter'}), 400
    
    profile_info, error = get_instagram_profile(username)
    if error:
        return jsonify({'error': error}), 500
    
    return jsonify(profile_info)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
