from flask import Blueprint, jsonify, send_from_directory
import os
import random
import json

details_bp = Blueprint('details', __name__)

DETAILS_FILE = os.path.join(os.getcwd(), 'chat', 'details.json')

def load_details():
    with open(DETAILS_FILE, 'r') as f:
        details = json.load(f)
    return details

DETAILS = load_details()

@details_bp.route('/details/<category>', methods=['GET'])
def get_random_fact(category):
    try:
        if category in DETAILS:
            facts = DETAILS[category]
            random_fact = random.choice(facts)
            return jsonify({"fact": random_fact})
        else:
            return f"No facts found for category '{category}'", 404
    except IndexError:
        return f"No facts found for category '{category}'", 404
    except Exception as e:
        return str(e), 500
