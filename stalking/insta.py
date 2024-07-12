import instaloader

def get_instagram_profile(username):
    L = instaloader.Instaloader()
    
    try:
        profile = instaloader.Profile.from_username(L.context, username)
    except instaloader.exceptions.ProfileNotExistsException:
        return None, "Profile does not exist"
    except instaloader.exceptions.InstaloaderException as e:
        return None, f"Failed to fetch profile: {str(e)}"
    
    profile_info = {
        'username': profile.username,
        'full_name': profile.full_name,
        'followers_count': profile.followers,
        'following_count': profile.followees,
        'post_count': profile.mediacount,
        'profile_pic_url': profile.profile_pic_url
    }
    
    return profile_info, None
