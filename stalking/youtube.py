import requests
from bs4 import BeautifulSoup

def get_youtube_thumbnail(video_url):
    try:
        response = requests.get(video_url)
        if response.status_code != 200:
            return None, 'Failed to fetch video page'
        
        soup = BeautifulSoup(response.content, 'html.parser')
        thumbnail_url = soup.find('meta', property='og:image')['content']
        
        if not thumbnail_url:
            return None, 'Failed to fetch thumbnail'
        
        return thumbnail_url, None
    except Exception as e:
        return None, str(e)
