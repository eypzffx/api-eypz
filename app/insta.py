from flask import Blueprint, request, jsonify
import instaloader

insta_bp = Blueprint('insta', __name__)

def download_instagram_media(url):
    loader = instaloader.Instaloader()
    media_urls = []

    try:
        post = instaloader.Post.from_shortcode(loader.context, url.split("/")[-2])
        if post.is_video:
            media_urls.append(post.video_url)
        else:
            media_urls.append(post.url)

        for sidecar_node in post.get_sidecar_nodes():
            if sidecar_node.is_video:
                media_urls.append(sidecar_node.video_url)
            else:
                media_urls.append(sidecar_node.display_url)
    except Exception as e:
        print(f"Error downloading post: {e}")
        pass

    try:
        profile = instaloader.Profile.from_username(loader.context, url.split("/")[-2])
        stories = loader.get_stories(userids=[profile.userid])
        for story in stories:
            for item in story.get_items():
                if item.video_url:
                    media_urls.append(item.video_url)
                else:
                    media_urls.append(item.url)
    except Exception as e:
        print(f"Error downloading stories: {e}")
        pass

    return media_urls

@insta_bp.route('/download', methods=['GET'])
def insta_downloader():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "URL parameter is required"}), 400

    media_urls = download_instagram_media(url)
    if media_urls:
        return jsonify({"media_urls": media_urls}), 200
    else:
        return jsonify({"error": "Failed to download media"}), 500
