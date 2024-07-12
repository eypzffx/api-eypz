# stalking/insta.py

import instaloader

def get_instagram_profile(username):
    L = instaloader.Instaloader()

    try:
        profile = instaloader.Profile.from_username(L.context, username)
    except instaloader.exceptions.ProfileNotExistsException:
        return None, "Profile does not exist"
    except instaloader.exceptions.InstaloaderException as e:
        return None, f"Failed to fetch profile: {str(e)}"

    # Debug prints to check what profile object contains
    print(f"Username: {profile.username}")
    print(f"Full Name: {profile.full_name}")
    print(f"Biography: {profile.biography}")
    print(f"Followers: {profile.followers}")
    print(f"Following: {profile.followees}")
    print(f"Posts: {profile.mediacount}")
    print(f"Profile Pic URL: {profile.profile_pic_url}")

    profile_info = {
        'username': profile.username,
        'full_name': profile.full_name,
        'biography': profile.biography,  # Include biography field
        'followers_count': profile.followers,
        'following_count': profile.followees,
        'post_count': profile.mediacount,
        'profile_pic_url': profile.profile_pic_url
    }

    return profile_info, None
