from flask import Flask, jsonify, send_from_directory, render_template, request
import os
import random
import json
import requests
import re

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
        return jsonify({'error': 'Missing URL parameter'}), 400

    video_id = extract_video_id(video_url)
    if not video_id:
        return jsonify({'error': 'Invalid YouTube URL'}), 400

    thumbnail_url = f'https://img.youtube.com/vi/{video_id}/maxresdefault.jpg'

    try:
        response = requests.get(thumbnail_url)
        if response.status_code == 200:
            return response.content, 200, {'Content-Type': 'image/jpeg'}
        else:
            return jsonify({'error': 'Failed to fetch thumbnail'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def extract_video_id(url):
    # Regular expression to extract video ID from YouTube URL
    regex = r"(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})"
    match = re.search(regex, url)
    if match:
        return match.group(1)
    return None

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
