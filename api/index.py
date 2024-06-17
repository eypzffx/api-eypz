from flask import Flask, Response
import random
import requests
import json

app = Flask(__name__)

with open('../video.json', 'r') as file:
    urls = json.load(file)

#home
@app.route('/')
def home():
    return 'Api is running somewhere!'
 
#random videos    
@app.route('/videos', methods=['GET'])
def video():
    selected_url = random.choice(urls)
    response = requests.get(selected_url, stream=True)
    return Response(response.iter_content(chunk_size=1024), content_type=response.headers['content-type'])



#dont touch this thing
if __name__ == '__main__':
    app.run(port=3000)
