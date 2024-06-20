from flask import Flask, Response, stream_with_context
import random
import requests

app = Flask(__name__)

IronMan = [
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
    video_url = random.choice(IronMan)
    
    def generate():
        with requests.get(video_url, stream=True) as r:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    yield chunk
    
    return Response(stream_with_context(generate()), content_type='video/mp4', headers={"Access-Control-Allow-Origin": "*"})

if __name__ == '__main__':
    app.run(port=3000, debug=True)
