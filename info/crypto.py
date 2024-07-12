import requests
from flask import jsonify

def get_crypto():
    crypto_url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd"
    response = requests.get(crypto_url)
    if response.status_code == 200:
        data = response.json()
        crypto_info = {
            "bitcoin": data["bitcoin"]["usd"],
            "ethereum": data["ethereum"]["usd"]
        }
        return jsonify(crypto_info)
    else:
        return jsonify({'error': 'Failed to fetch cryptocurrency data'}), 500
