from flask import Flask, send_from_directory
import os
import random

app = Flask(__name__)

# Define the directory where your video files are stored
VIDEO_DIRECTORY = os.path.join(os.getcwd(), 'video')

# List all video files in the VIDEO_DIRECTORY
video_files = os.listdir(VIDEO_DIRECTORY)

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

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
