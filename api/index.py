from flask import Flask, Response
import random
import requests
import json

app = Flask(__name__)

eypz = [
    "https://aemt.me/file/1wyRPkzAYgts.mp4",
    "https://i.imgur.com/8QiXNLt.mp4"
]

# Home 
@app.route('/')
def home():
    return 'API is running somewhere!'

#vidoe
@app.route('/video', methods=['GET'])
def anime():
    video_url = random.choice(eypz)
    
    def generate():
        with requests.get(video_url, stream=True) as r:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    yield chunk
    
    return Response(generate(), content_type='video/mp4')

if __name__ == '__main__':
    app.run(port=3000)
