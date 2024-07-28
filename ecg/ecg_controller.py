from flask import Blueprint, request, render_template, current_app
from werkzeug.utils import secure_filename
from utils import files
import parse_ecg
import os

bp = Blueprint('ecg', __name__, url_prefix='/ecg')


@bp.route('/download/<filename>')
def download_file(filename):
    samples = parse_ecg.read_24bit_samples(filename)
    return samples


@bp.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
        if file and files.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            return f'File {filename} uploaded successfully'
    return render_template('index.html')
