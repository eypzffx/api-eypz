import requests

SPOTIFY_SEARCH_API_URL = "https://api.maher-zubair.tech/search/spotify?q="

def search_spotify_tracks(query):
    try:
        response = requests.get(f"{SPOTIFY_SEARCH_API_URL}{query}")
        data = response.json()

        if response.status_code != 200:
            return {'error': 'Failed to fetch data from external API'}, response.status_code

        results = []
        for item in data.get('tracks', {}).get('items', []):
            track_info = {
                'title': item['name'],
                'artist': ', '.join(artist['name'] for artist in item['artists']),
                'album': item['album']['name'],
                'link': item['external_urls']['spotify'],
            }
            results.append(track_info)

        return results, 200
    except Exception as e:
        return {'error': str(e)}, 500
