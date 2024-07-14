from flask import Flask
from app.lyrics import lyrics_bp
from app.media import media_bp
from app.youtube import youtube_bp
from app.instagram import instagram_bp
from app.weather import weather_bp
from app.crypto import crypto_bp
from app.search import search_bp
from app.nsfw import nsfw_bp

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100 MB upload limit

# Register Blueprints
app.register_blueprint(lyrics_bp)
app.register_blueprint(media_bp)
app.register_blueprint(youtube_bp)
app.register_blueprint(instagram_bp)
app.register_blueprint(weather_bp)
app.register_blueprint(crypto_bp)
app.register_blueprint(search_bp)
app.register_blueprint(nsfw_bp)

app.route('/')
def index():
    return render_template('index.html')
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
