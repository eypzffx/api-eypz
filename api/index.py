from flask import Flask, Response
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
    app.logger.info(f"Selected video URL: {video_url}")

    def generate():
        try:
            with requests.get(video_url, stream=True) as r:
                r.raise_for_status()
                content_length = r.headers.get('Content-Length')
                app.logger.info(f"Content-Length: {content_length}")
                
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        yield chunk
        except requests.RequestException as e:
            app.logger.error(f"Error fetching video: {e}")
            yield b''

    return Response(generate(), content_type='video/mp4')

if __name__ == '__main__':
    app.run(port=3000, debug=True)
