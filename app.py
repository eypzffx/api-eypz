from flask import Flask, request, jsonify, send_from_directory, send_file
import os
import random
import json

app = Flask(__name__)

# Define the directories where your video and image files are stored
VIDEO_DIRECTORY = os.path.join(os.getcwd(), 'video')
IMAGE_DIRECTORY = os.path.join(os.getcwd(), 'image')
TSUNADE_DIRECTORY = os.path.join(os.getcwd(), 'tsunade')
NARUTO_DIRECTORY = os.path.join(os.getcwd(), 'naruto')

# List all video and image files in their respective directories
video_files = os.listdir(VIDEO_DIRECTORY)
image_files = os.listdir(IMAGE_DIRECTORY)
tsunade_files = os.listdir(TSUNADE_DIRECTORY)
naruto_files = os.listdir(NARUTO_DIRECTORY)

# Load cat facts from JSON file in the 'chat' folder
json_path = os.path.join(os.getcwd(), 'chat', 'cat_fact.json')
with open(json_path, 'r') as f:
    cat_data = json.load(f)
    cat_facts = cat_data['facts']

@app.route('/')
def home():
    return send_file('index.html')

@app.route('/anime', methods=['GET'])
def serve_random_video():
    try:
        random_video = random.choice(video_files)
        return send_from_directory(VIDEO_DIRECTORY, random_video)
    except IndexError:
        return "No videos found", 404
    except Exception as e:
        return str(e), 500

@app.route('/image', methods=['GET'])
def serve_random_image():
    try:
        random_image = random.choice(image_files)
        return send_from_directory(IMAGE_DIRECTORY, random_image)
    except IndexError:
        return "No images found", 404
    except Exception as e:
        return str(e), 500

@app.route('/tsunade', methods=['GET'])
def serve_random_tsunade():
    try:
        random_tsunade = random.choice(tsunade_files)
        return send_from_directory(TSUNADE_DIRECTORY, random_tsunade)
    except IndexError:
        return "No Tsunade images found", 404
    except Exception as e:
        return str(e), 500

@app.route('/naruto', methods=['GET'])
def serve_random_naruto():
    try:
        random_naruto = random.choice(naruto_files)
        return send_from_directory(NARUTO_DIRECTORY, random_naruto)
    except IndexError:
        return "No Naruto images found", 404
    except Exception as e:
        return str(e), 500

@app.route('/cat-fact', methods=['GET'])
def get_random_cat_fact():
    try:
        random_fact = random.choice(cat_facts)
        return jsonify({'fact': random_fact})
    except IndexError:
        return "No cat facts found", 404
    except Exception as e:
        return str(e), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
