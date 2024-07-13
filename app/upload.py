from flask import Blueprint, jsonify, request, send_from_directory, url_for
from werkzeug.utils import secure_filename
import os
import uuid

upload_bp = Blueprint('upload', __name__)

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp3', 'wav', 'mp4', 'mov', 'avi'}
MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100 MB upload limit

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@upload_bp.route('/upload', methods=['POST'])
def upload_file():
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
        file_url = url_for('upload.uploaded_file', filename=unique_filename, _external=True)
        return jsonify({"url": file_url}), 200
    else:
        return jsonify({"error": "File type not allowed"}), 400

@upload_bp.route('/uploads/<filename>', methods=['GET'])
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@upload_bp.route('/url/upload', methods=['GET', 'POST'])
def upload_page():
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
            file_url = url_for('upload.uploaded_file', filename=unique_filename, _external=True)
            return jsonify({"url": file_url}), 200
        else:
            return jsonify({"error": "File type not allowed"}), 400
    return '''
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <title>Upload File</title>
      </head>
      <body>
        <h1>Upload File</h1>
        <form method="post" enctype="multipart/form-data">
          <input type="file" name="file">
          <input type="submit" value="Upload">
        </form>
      </body>
    </html>
    '''
