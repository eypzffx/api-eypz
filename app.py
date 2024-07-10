from flask import Flask, request, jsonify, send_from_directory
import os
import random
import openai

app = Flask(__name__)

# Define the directories where your video and image files are stored
VIDEO_DIRECTORY = os.path.join(os.getcwd(), 'video')
IMAGE_DIRECTORY = os.path.join(os.getcwd(), 'image')
TSUNADE_DIRECTORY = os.path.join(os.getcwd(), 'tsunade')

# List all video and image files in their respective directories
video_files = os.listdir(VIDEO_DIRECTORY)
image_files = os.listdir(IMAGE_DIRECTORY)
tsunade_files = os.listdir(TSUNADE_DIRECTORY)

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
        return "No tsunade images found", 404
    except Exception as e:
        return str(e), 500

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    if 'message' not in data:
        return jsonify({'error': 'No message provided'}), 400
    
    message = data['message']
    
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=message,
            max_tokens=50
        )
        return jsonify({'response': response.choices[0].text.strip()})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
