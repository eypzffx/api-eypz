from flask import Flask, Response
import random
import requests
import json

app = Flask(__name__)

IronMan = [
    "https://cdn.discordapp.com/attachments/947033103988314143/1252355487706648710/VID-20240608-WA0044.mp4?ex=6671ea6f&is=667098ef&hm=a702c6325ed8e2df64956861c33495ca1ba90340e946735ecb91c2b29c705384&",
    "https://cdn.discordapp.com/attachments/947033103988314143/1252360857946689717/20240418152629633.mp4?ex=6671ef70&is=66709df0&hm=2ec880e4f4c18631dcf189c273c4c928173eaf8a9c9f96ca7c01b30955cab9bf&"
]

# Home 
@app.route('/')
def home():
    return 'API is running somewhere!'

#vidoe
@app.route('/video', methods=['GET'])
def anime():
    video_url = random.choice(IronMan)
    
    def generate():
        with requests.get(video_url, stream=True) as r:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    yield chunk
    
    return Response(generate(), content_type='video/mp4')

if __name__ == '__main__':
    app.run(port=3000)
