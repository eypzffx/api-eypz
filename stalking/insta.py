import requests
from bs4 import BeautifulSoup

def get_instagram_profile(username):
    url = f'https://www.instagram.com/{username}/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return None, 'Failed to fetch profile page'

        soup = BeautifulSoup(response.content, 'html.parser')
        script_tag = soup.find('script', string=lambda t: t and 'window._sharedData' in t)

        if not script_tag:
            return None, 'Failed to find shared data script tag'

        shared_data = script_tag.string.split('window._sharedData = ')[1].rstrip(';')
        data = json.loads(shared_data)
        user_info = data['entry_data']['ProfilePage'][0]['graphql']['user']

        profile_info = {
            'username': user_info['username'],
            'full_name': user_info['full_name'],
            'bio': user_info['biography'],
            'followers': user_info['edge_followed_by']['count'],
            'following': user_info['edge_follow']['count'],
            'posts': user_info['edge_owner_to_timeline_media']['count'],
            'profile_pic_url': user_info['profile_pic_url_hd']
        }
        return profile_info, None
    except Exception as e:
        return None, str(e)
