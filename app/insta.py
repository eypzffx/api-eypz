from flask import Blueprint, request, jsonify
import instaloader
import re

insta_bp = Blueprint('insta', __name__)

@bp.route('/insta_story', methods=['GET'])
def download_insta_media():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "URL parameter is required"}), 400

    L = instaloader.Instaloader()

    try:
        # Login with the provided credentials
        L.login('eypzizumi', 'rihaeypz')
    except Exception as e:
        return jsonify({"error": "Login failed: " + str(e)}), 500

    try:
        media_urls = []
        
        if 'stories' in url:
            # Story URL
            username_match = re.search(r'instagram.com/stories/(.*?)/', url)
            if not username_match:
                return jsonify({"error": "Invalid stories URL"}), 400
            username = username_match.group(1)
            profile = instaloader.Profile.from_username(L.context, username)

            for story in L.get_stories(userids=[profile.userid]):
                for item in story.get_items():
                    if item.is_video:
                        media_urls.append(item.video_url)
                    else:
                        media_urls.append(item.url)
        else:
            # Regular post URL
            shortcode_match = re.search(r'instagram.com/p/([^/]+)/', url)
            if not shortcode_match:
                return jsonify({"error": "Invalid post URL"}), 400
            shortcode = shortcode_match.group(1)
            post = instaloader.Post.from_shortcode(L.context, shortcode)

            if post.typename == 'GraphImage':
                media_urls.append(post.url)
            elif post.typename == 'GraphVideo':
                media_urls.append(post.video_url)
            elif post.typename == 'GraphSidecar':
                for sidecar_node in post.get_sidecar_nodes():
                    if sidecar_node.is_video:
                        media_urls.append(sidecar_node.video_url)
                    else:
                        media_urls.append(sidecar_node.display_url)

        return jsonify({"media_urls": media_urls})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
