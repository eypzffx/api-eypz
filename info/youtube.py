import requests
import isodate

YOUTUBE_API_KEY = 'AIzaSyCB688y-WEp2haiqYHwgcxfXOAQ9Q1dtjM'
YOUTUBE_API_URL = 'https://www.googleapis.com/youtube/v3/search'
YOUTUBE_VIDEO_DETAILS_URL = 'https://www.googleapis.com/youtube/v3/videos'

def convert_duration(duration):
    duration = isodate.parse_duration(duration)
    total_seconds = int(duration.total_seconds())
    minutes, seconds = divmod(total_seconds, 60)
    return f"{minutes}:{seconds:02d}"

def search_youtube_videos(query):
    try:
        search_params = {
            'part': 'snippet',
            'q': query,
            'type': 'video',
            'maxResults': 15,
            'key': YOUTUBE_API_KEY
        }
        search_response = requests.get(YOUTUBE_API_URL, params=search_params)
        search_data = search_response.json()

        if 'error' in search_data:
            return {'error': search_data['error']['message']}, search_data['error']['code']

        video_ids = [item['id']['videoId'] for item in search_data['items']]

        video_params = {
            'part': 'contentDetails,snippet',
            'id': ','.join(video_ids),
            'key': YOUTUBE_API_KEY
        }
        video_response = requests.get(YOUTUBE_VIDEO_DETAILS_URL, params=video_params)
        video_data = video_response.json()

        if 'error' in video_data:
            return {'error': video_data['error']['message']}, video_data['error']['code']

        results = []
        for item in video_data['items']:
            video_info = {
                'title': item['snippet']['title'],
                'link': f"https://www.youtube.com/watch?v={item['id']}",
                'duration': convert_duration(item['contentDetails']['duration'])
            }
            results.append(video_info)

        return results, 200
    except Exception as e:
        return {'error': str(e)}, 500
