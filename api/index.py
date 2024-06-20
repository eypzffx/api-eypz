from flask import Flask, Response, stream_with_context
import random
import requests
import json

app = Flask(__name__)

def load_video_urls():
    with open('video.json') as f:
        data = json.load(f)
    return data["IronMan"]

# Home 
@app.route('/')
def home():
    return 'API is running somewhere!'

# Video
@app.route('/video', methods=['GET'])
def anime():
    video_urls = load_video_urls()
    video_url = random.choice(video_urls)
    
    def generate():
        with requests.get(video_url, stream=True) as r:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    yield chunk
    
    return Response(stream_with_context(generate()), content_type='video/mp4', headers={"Access-Control-Allow-Origin": "*"})

if __name__ == '__main__':
    app.run(port=3000, debug=True)
