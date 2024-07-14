# app/lyrics.py
from flask import Blueprint, jsonify, request
import lyricsgenius

lyrics_bp = Blueprint('lyrics', __name__)
genius = lyricsgenius.Genius("UCPfLPaO-yEFTrzwgxsNgPN0JaZr8rUnWhLXjA4w5WmUP9rFp1ueGXPPcRqW6Jsa")

@lyrics_bp.route('/lyrics', methods=['GET'])
def get_lyrics():
    query = request.args.get('q')

    if not query:
        return jsonify({'error': 'Missing query parameter `q`'}), 400

    try:
        song = genius.search_song(query)
        if song:
            response = {
                'title': song.title,
                'artist': song.artist,
                'lyrics': song.lyrics
            }
            return jsonify(response)
        else:
            return jsonify({'error': 'Lyrics not found for the given query'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
