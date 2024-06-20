from flask import Flask, Response
import random
import requests
import json

app = Flask(__name__)

Eypz = [
  "https://i.imgur.com/wVHPACz.mp4",
  "https://i.imgur.com/NErSHY5.mp4",
  "https://i.imgur.com/CUZf2Cf.mp4",
  "https://i.imgur.com/WqckfnX.mp4",
  "https://i.imgur.com/Z2cwsrz.mp4",
  "https://i.imgur.com/5gL4cZo.mp4",
  "https://i.imgur.com/ZLkPIsY.mp4",
  "https://i.imgur.com/kLedgdR.mp4",
  "https://i.imgur.com/KUGRx8b.mp4",
  "https://i.imgur.com/h1UKkcP.mp4",
  "https://i.imgur.com/nWJdaGX.mp4",
  "https://i.imgur.com/vdxn09c.mp4",
  "https://i.imgur.com/fb1VAlr.mp4",
  "https://i.imgur.com/bheqlD7.mp4",
  "https://i.imgur.com/uWhr4iL.mp4",
  "https://i.imgur.com/zGzFerK.mp4",
  "https://i.imgur.com/3Cv02cz.mp4",
  "https://i.imgur.com/LHW3T60.mp4",
  "https://i.imgur.com/IUtst5x.mp4",
  "https://i.imgur.com/M4rX4PB.mp4",
  "https://i.imgur.com/sO3pNoF.mp4",
  "https://i.imgur.com/RHTIEKB.mp4",
  "https://i.imgur.com/P7NEpNd.mp4",
  "https://i.imgur.com/k4HVHC9.mp4",
  "https://i.imgur.com/gnd5eGE.mp4",
  "https://i.imgur.com/JBoRyy6.mp4",
  "https://i.imgur.com/aF8x8zb.mp4",
  "https://i.imgur.com/3rNFcgE.mp4",
  "https://i.imgur.com/9ec6N3l.mp4",
  "https://i.imgur.com/iERiqLB.mp4",
  "https://i.imgur.com/WK62Btn.mp4",
  "https://i.imgur.com/PsbcOF9.mp4",
  "https://i.imgur.com/0Ysn9Ol.mp4",
  "https://i.imgur.com/1D4a8Fj.mp4"
]

# Home 
@app.route('/')
def home():
    return 'API is running somewhere!'

#vidoe
@app.route('/video', methods=['GET'])
def anime():
    video_url = random.choice(Eypz)
    
    def generate():
        with requests.get(video_url, stream=True) as r:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    yield chunk
    
    return Response(generate(), content_type='video/mp4')

if __name__ == '__main__':
    app.run(port=3000)
