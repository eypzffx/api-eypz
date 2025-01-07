from flask import Blueprint, jsonify
import requests

# Create a blueprint for IP Fetching
ip_bp = Blueprint('ip', __name__)

@ip_bp.route('/ip', methods=['GET'])
def get_ip():
    try:
        ip_response = requests.get('https://api.ipify.org?format=json')
        if ip_response.status_code == 200:
            ip_data = ip_response.json()
            return jsonify({"ip": ip_data['ip']})  # Return the public IP
        else:
            return jsonify({"error": "Unable to fetch IP"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
