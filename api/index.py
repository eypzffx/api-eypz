from flask import Flask, Response, jsonify
import random
import requests

app = Flask(__name__)

eypz = [
    "https://aemt.me/file/1wyRPkzAYgts.mp4",
    "https://i.imgur.com/8QiXNLt.mp4"
]

# Home
@app.route('/')
def home():
    return 'API is running somewhere!'

# Video
@app.route('/video', methods=['GET'])
def anime():
    video_url = random.choice(eypz)
    print(f"Selected video URL: {video_url}")

    def generate():
        try:
            with requests.get(video_url, stream=True) as r:
                r.raise_for_status()
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        yield chunk
        except requests.RequestException as e:
            print(f"Error fetching video: {e}")
            yield b''

    return Response(generate(), content_type='video/mp4')

if __name__ == '__main__':
    app.run(port=3000, debug=True)
