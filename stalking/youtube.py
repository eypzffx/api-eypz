import requests
import re

def download_thumbnail(video_url):
    video_id = extract_video_id(video_url)
    if not video_id:
        return None, 'Invalid YouTube URL'

    thumbnail_url = f'https://img.youtube.com/vi/{video_id}/maxresdefault.jpg'

    try:
        response = requests.get(thumbnail_url)
        if response.status_code == 200:
            return thumbnail_url, None
        else:
            return None, 'Failed to fetch thumbnail'
    except Exception as e:
        return None, str(e)

def extract_video_id(url):
    regex = r"(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})"
    match = re.search(regex, url)
    if match:
        return match.group(1)
    return None
