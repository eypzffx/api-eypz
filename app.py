from flask import Flask, jsonify, send_from_directory
import os
import random
import json

app = Flask(__name__)

# Define the directories where your video and image files are stored
VIDEO_DIRECTORY = os.path.join(os.getcwd(), 'videos', 'naruto')
IMAGE_DIRECTORY_IMAGE = os.path.join(os.getcwd(), 'images', 'image')
IMAGE_DIRECTORY_CAT = os.path.join(os.getcwd(), 'images', 'cat')
IMAGE_DIRECTORY_TSUNADE = os.path.join(os.getcwd(), 'images', 'tsunade')
CAT_FACT_FILE = os.path.join(os.getcwd(), 'chat', 'cat_fact.json')
DETAILS_FILE = os.path.join(os.getcwd(), 'chat', 'details.json')

# List all video and image files in their respective directories
video_files = os.listdir(VIDEO_DIRECTORY)
image_files_image = os.listdir(IMAGE_DIRECTORY_IMAGE)
image_files_cat = os.listdir(IMAGE_DIRECTORY_CAT)
image_files_tsunade = os.listdir(IMAGE_DIRECTORY_TSUNADE)

# Function to load cat facts from JSON file
def load_cat_facts():
    with open(CAT_FACT_FILE, 'r') as f:
        cat_facts = json.load(f)
    return cat_facts['facts'] if 'facts' in cat_facts else []

# Load cat facts from JSON file
CAT_FACTS = load_cat_facts()

# Load details from JSON file
def load_details():
    with open(DETAILS_FILE, 'r') as f:
        details = json.load(f)
    return details

# Load details from JSON file
DETAILS = load_details()

@app.route('/naruto', methods=['GET'])
def serve_random_naruto_video():
    try:
        # Choose a random video file from the list
        random_video = random.choice(video_files)
        return send_from_directory(VIDEO_DIRECTORY, random_video)
    except IndexError:
        return "No Naruto videos found", 404
    except Exception as e:
        return str(e), 500

@app.route('/image', methods=['GET'])
def serve_random_image_image():
    try:
        # Choose a random image file from the list
        random_image = random.choice(image_files_image)
        return send_from_directory(IMAGE_DIRECTORY_IMAGE, random_image)
    except IndexError:
        return "No images found in 'image' directory", 404
    except Exception as e:
        return str(e), 500

@app.route('/cat', methods=['GET'])
def serve_random_image_cat():
    try:
        # Choose a random image file from the list
        random_image = random.choice(image_files_cat)
        return send_from_directory(IMAGE_DIRECTORY_CAT, random_image)
    except IndexError:
        return "No images found in 'cat' directory", 404
    except Exception as e:
        return str(e), 500

@app.route('/tsunade', methods=['GET'])
def serve_random_image_tsunade():
    try:
        # Choose a random image file from the list
        random_image = random.choice(image_files_tsunade)
        return send_from_directory(IMAGE_DIRECTORY_TSUNADE, random_image)
    except IndexError:
        return "No images found in 'tsunade' directory", 404
    except Exception as e:
        return str(e), 500

@app.route('/cat-fact', methods=['GET'])
def get_random_cat_fact():
    try:
        # Choose a random cat fact from the loaded JSON file
        random_fact = random.choice(CAT_FACTS)
        return jsonify({"fact": random_fact})
    except IndexError:
        return "No cat facts found", 404
    except Exception as e:
        return str(e), 500

@app.route('/details/<category>', methods=['GET'])
def get_random_fact(category):
    try:
        # Ensure the requested category exists in details.json
        if category in DETAILS:
            facts = DETAILS[category]
            # Choose a random fact from the category
            random_fact = random.choice(facts)
            return jsonify({"fact": random_fact})
        else:
            return f"No facts found for category '{category}'", 404
    except IndexError:
        return f"No facts found for category '{category}'", 404
    except Exception as e:
        return str(e), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
