from flask import Blueprint, request, redirect, url_for, jsonify, render_template
from werkzeug.utils import secure_filename
import os
import uuid

upload_bp = Blueprint('upload_bp', __name__, template_folder='templates')

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp3', 'wav', 'mp4', 'mov', 'avi'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@upload_bp.route('/url/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            unique_id = str(uuid.uuid4())
            file_extension = filename.rsplit('.', 1)[1].lower()
            unique_filename = f"{unique_id}.{file_extension}"
            file.save(os.path.join(UPLOAD_FOLDER, unique_filename))
            file_url = url_for('upload_bp.display_file', filename=unique_filename, _external=True)
            return jsonify({"url": file_url}), 200
        else:
            return jsonify({"error": "File type not allowed"}), 400
    return render_template('upload.html')

@upload_bp.route('/url/<filename>')
def display_file(filename):
    return redirect(url_for('static', filename='uploads/' + filename), code=301)
