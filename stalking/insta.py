from flask import Blueprint, request, jsonify
import instaloader

media_downloader_bp = Blueprint('media_downloader', __name__)

def download_instagram_media(url):
    loader = instaloader.Instaloader()
    media_urls = []

    try:
        # For posts and reels
        shortcode = url.split("/")[-2]
        post = instaloader.Post.from_shortcode(loader.context, shortcode)
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
    except Exception as e:
        print(f"Failed to download post/reel: {e}")

    try:
        # For stories
        shortcode = url.split("/")[-2]
        profile = instaloader.Profile.from_username(loader.context, shortcode)
        stories = loader.get_stories(userids=[profile.userid])
        for story in stories:
            for item in story.get_items():
                if item.video_url:
                    media_urls.append(item.video_url)
                else:
                    media_urls.append(item.url)
    except Exception as e:
        print(f"Failed to download stories: {e}")

    return media_urls

@media_downloader_bp.route('/download', methods=['GET'])
def download_media():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "No URL provided."}), 400

    media_urls = download_instagram_media(url)
    if not media_urls:
        return jsonify({"error": "Failed to download media."}), 500

    return jsonify({"media_urls": media_urls})
