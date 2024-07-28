from flask import Flask, render_template
from flask_cors import CORS

# Import all existing blueprints
from app.lyrics import lyrics_bp
from app.media import media_bp
from app.youtube import youtube_bp
from app.instagram import instagram_bp  # Assuming this is for other Instagram functionalities
from app.weather import weather_bp
from app.crypto import crypto_bp
from app.search import search_bp
from app.nsfw import nsfw_bp
from app.details import details_bp
from app.trivia import trivia_bp
from app.shorten import shorten_bp
from app.image_search import image_search_bp
from app.insta import insta_bp  # Import the new Instagram downloader blueprint

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Register all existing blueprints
app.register_blueprint(lyrics_bp)
app.register_blueprint(media_bp)
app.register_blueprint(youtube_bp)
app.register_blueprint(instagram_bp)
app.register_blueprint(weather_bp)
app.register_blueprint(crypto_bp)
app.register_blueprint(search_bp)
app.register_blueprint(nsfw_bp)
app.register_blueprint(details_bp)
app.register_blueprint(trivia_bp)
app.register_blueprint(shorten_bp)
app.register_blueprint(image_search_bp)
app.register_blueprint(insta_bp, url_prefix='/insta')  # Register the new Instagram downloader blueprint

# Route for index page
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
