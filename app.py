from flask import Flask, send_from_directory
import os
import random

app = Flask(__name__)

# Define the directories where your video and image files are stored
VIDEO_DIRECTORY = os.path.join(os.getcwd(), 'video')
IMAGE_DIRECTORY = os.path.join(os.getcwd(), 'image')
Tsunade = os.path.join(os.getcwd(), 'tsunade')

# List all video and image files in their respective directories
video_files = os.listdir(VIDEO_DIRECTORY)
image_files = os.listdir(IMAGE_DIRECTORY)
Tsunade_files = os.listdir(Tsunade)

@app.route('/anime', methods=['GET'])
def serve_random_video():
    try:
        # Choose a random video file from the list
        random_video = random.choice(video_files)
        return send_from_directory(VIDEO_DIRECTORY, random_video)
    except IndexError:
        return "No videos found", 404
    except Exception as e:
        return str(e), 500

@app.route('/image', methods=['GET'])
def serve_random_image():
    try:
        # Choose a random image file from the list
        random_image = random.choice(image_files)
        return send_from_directory(IMAGE_DIRECTORY, random_image)
    except IndexError:
        return "No images found", 404
    except Exception as e:
        return str(e), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

@app.route('/tsunade', methods=['GET'])
def serve_random_tsunade():
    try:
        # Choose a random image file from the list
        random_tsunade = random.choice(Tsunade_files)
        return send_from_directory(Tsunade, random_tsunade)
    except IndexError:
        return "No images found", 404
    except Exception as e:
        return str(e), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
