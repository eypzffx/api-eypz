import base64
import requests
from flask import Blueprint, request, jsonify

# Create a Blueprint for the Spotify search
spotifys_bp = Blueprint('spotifys', __name__)

# Replace with your Spotify API credentials
CLIENT_ID = '27fdcd40e50f4e4d8315e27adc25f48d'
CLIENT_SECRET = '4d0c177c1c94409782fb5cdf2157ec91'

# Function to get the access token from Spotify API
def get_spotify_access_token(client_id, client_secret):
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": f"Basic {base64.b64encode(f'{client_id}:{client_secret}'.encode()).decode()}"
    }
    data = {"grant_type": "client_credentials"}
    response = requests.post(url, headers=headers, data=data)
    return response.json()['access_token']

# Function to search Spotify
def search_spotify(query, access_token):
    url = f"https://api.spotify.com/v1/search?q={query}&type=track,album,artist,playlist&limit=10"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(url, headers=headers)
    return response.json()

# Get access token
access_token = get_spotify_access_token(CLIENT_ID, CLIENT_SECRET)

# Define the search endpoint in the Blueprint
@spotifys_bp.route('/spotify/search', methods=['GET'])
def search():
    # Get the search query parameter
    query = request.args.get('q')
    if not query:
        return jsonify({"error": "Query parameter 'q' is required"}), 400

    # Call the search function
    results = search_spotify(query, access_token)

    # Return the search results as JSON
    return jsonify(results)
