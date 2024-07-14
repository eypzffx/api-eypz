# app/crypto.py
from flask import Blueprint
from info.crypto import get_crypto

crypto_bp = Blueprint('crypto', __name__)

@crypto_bp.route('/info/crypto', methods=['GET'])
def info_crypto():
    return get_crypto()
