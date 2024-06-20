from flask import Flask, Response
import random
import requests
import json

app = Flask(__name__)

with open('video.json', 'r') as f:
    video_urls = json.load(f)

#home
@app.route('/')
def home():
    return 'API is running somewhere!'

#vidoe 
@app.route('/video', methods=['GET'])
def anime():
    video_url = random.choice(video_urls)
    
    def generate():
        with requests.get(video_url, stream=True) as r:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    yield chunk
    
    return Response(generate(), content_type='video/mp4')

if __name__ == '__main__':
    app.run(port=3000)
