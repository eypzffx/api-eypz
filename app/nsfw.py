# app/nsfw.py
from flask import Blueprint, jsonify
import random
import os
import json

nsfw_bp = Blueprint('nsfw', __name__)

NSFW_WAIFU_FILE = os.path.join(os.getcwd(), 'nsfw', 'waifu.json')
NSFW_NEKO_FILE = os.path.join(os.getcwd(), 'nsfw', 'neko.json')

def load_waifu_data():
    with open(NSFW_WAIFU_FILE, 'r') as f:
        waifu_data = json.load(f)
    return waifu_data

def load_neko_data():
    with open(NSFW_NEKO_FILE, 'r') as f:
        neko_data = json.load(f)
    return neko_data

WAIFU_DATA = load_waifu_data()
NEKO_DATA = load_neko_data()

@nsfw_bp.route('/nsfw/waifu', methods=['GET'])
def serve_random_nsfw_waifu():
    try:
        random_waifu = random.choice(WAIFU_DATA)['url']
        return jsonify({"url": random_waifu})
    except IndexError:
        return "No NSFW waifu data found", 404
    except Exception as e:
        return str(e), 500

@nsfw_bp.route('/nsfw/neko', methods=['GET'])
def serve_random_nsfw_neko():
    try:
        random_neko = random.choice(NEKO_DATA)['url']
        return jsonify({"url": random_neko})
    except IndexError:
        return "No NSFW neko data found", 404
    except Exception as e:
        return str(e), 500
