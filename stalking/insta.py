# stalking/insta.py

import requests

def get_instagram_profile(username):
    try:
        url = f'https://www.instagram.com/{username}/?__a=1'
        response = requests.get(url)
        response.raise_for_status()
        profile_data = response.json()

        # Parse the profile data and extract relevant information
        profile_info = {
            'username': username,
            'full_name': profile_data['graphql']['user']['full_name'],
            'profile_pic_url': profile_data['graphql']['user']['profile_pic_url_hd'],
            'biography': profile_data['graphql']['user']['biography'],
            'follower_count': profile_data['graphql']['user']['edge_followed_by']['count'],
            'following_count': profile_data['graphql']['user']['edge_follow']['count']
            # Add more fields as needed
        }

        return profile_info, None

    except requests.exceptions.HTTPError as http_err:
        error_message = f"HTTP error occurred: {http_err}"
        return None, error_message

    except Exception as err:
        error_message = f"An error occurred: {err}"
        return None, error_message
