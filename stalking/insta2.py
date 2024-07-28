import instaloader

def download_instagram_media(url):
    loader = instaloader.Instaloader()
    media_urls = []

    try:
        # For posts and reels
        post = instaloader.Post.from_shortcode(loader.context, url.split("/")[-2])
        if post.is_video:
            media_urls.append(post.video_url)
        else:
            media_urls.append(post.url)

        # If the post has multiple media (like a carousel)
        for sidecar_node in post.get_sidecar_nodes():
            if sidecar_node.is_video:
                media_urls.append(sidecar_node.video_url)
            else:
                media_urls.append(sidecar_node.display_url)
    except:
        pass

    try:
        # For stories
        story_shortcode = url.split("/")[-2]
        profile = instaloader.Profile.from_username(loader.context, story_shortcode)
        stories = loader.get_stories(userids=[profile.userid])
        for story in stories:
            for item in story.get_items():
                if item.video_url:
                    media_urls.append(item.video_url)
                else:
                    media_urls.append(item.url)
    except:
        pass

    return media_urls
