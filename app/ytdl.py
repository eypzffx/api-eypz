from flask import Blueprint, request, jsonify
import requests
import os

# Define the Blueprint
ytdl_bp = Blueprint('ytdl', __name__)

@ytdl_bp.route('/ytdl', methods=['GET'])
def ytdl():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'URL parameter is required'}), 400

    # Load API key from environment variables
    api_key = os.getenv('API_KEY', 'eypz-izumi')  # Default to 'eypz-izumi' if not set

    # Build the request URL with the new endpoint
    request_url = f'https://api.betabotz.eu.org/api/download/allin?url={url}&apikey={api_key}'

    try:
        # Send the request to the external server
        response = requests.get(request_url)
        response.raise_for_status()  # Raise an error for bad responses

        # Get the JSON response from the external server
        data = response.json()

        # Ensure the expected keys are in the response
        if "result" not in data:
            return jsonify({'error': 'Invalid response from the external API'}), 500

        # Modify the 'creator' field to 'Eypz God' and keep the rest of the information
        result = {
            "status": data.get("status"),
            "creator": "Eypz God",  # Overriding creator field
            "result": {
                "title": data["result"].get("title"),
                "description": data["result"].get("description"),
                "source": data["result"].get("source"),
                "duration": data["result"].get("duration"),
                "thumb": data["result"].get("thumb"),
                "mp3": data["result"].get("mp3"),
                "mp4": data["result"].get("mp4"),
            }
        }

        # Return the modified JSON response
        return jsonify(result)

    except requests.RequestException as e:
        return jsonify({'error': 'Request to external API failed', 'details': str(e)}), 500
    except ValueError as e:
        return jsonify({'error': 'Invalid JSON response from external API', 'details': str(e)}), 500
    except KeyError as e:
        return jsonify({'error': 'Missing data in external API response', 'details': str(e)}), 500
