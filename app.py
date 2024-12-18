from flask import Flask, render_template
from flask_cors import CORS

# Import all existing blueprints
from app.aio import aio_bp
from app.media import media_bp
from app.youtube import youtube_bp  # Import the Instagram blueprint
from app.weather import weather_bp
from app.crypto import crypto_bp
from app.nsfw import nsfw_bp
from app.details import details_bp
from app.trivia import trivia_bp
from app.shorten import shorten_bp
from app.spotify import spotify_bp
from app.pin import pin_bp
from app.ytdl import ytdl_bp
from upload.routes import upload_bp
from html_files.temp import html_bp

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/')
def index():
    return render_template('index.html')

# Register all existing blueprints
app.register_blueprint(media_bp)
app.register_blueprint(youtube_bp)  # Register the Instagram blueprint
app.register_blueprint(weather_bp)
app.register_blueprint(crypto_bp)
app.register_blueprint(nsfw_bp)
app.register_blueprint(details_bp)
app.register_blueprint(trivia_bp)
app.register_blueprint(shorten_bp)
app.register_blueprint(spotify_bp)
app.register_blueprint(pin_bp)
app.register_blueprint(aio_bp)
app.register_blueprint(ytdl_bp)
app.register_blueprint(upload_bp)
app.register_blueprint(html_bp)

# Route for index page
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
