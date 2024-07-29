from flask import Blueprint, request, render_template, current_app, session
from werkzeug.utils import secure_filename
from utils import validate_file_extensions, read_raw_file_size
from ecg import parse_ecg
import os

bp = Blueprint('ecg', __name__, url_prefix='/ecg')


@bp.route('/download/<filename>')
def download_file(filename):
    samples = parse_ecg.read_24bit_samples(filename)
    return samples


@bp.route('/', methods=['GET', 'POST'])
def compress_file():
    if request.method == 'POST':

        # Check for username field, we'll use it to set a session variable.
        # We may use session variables to identify the user's files when performing the download.
        if 'name' not in request.form:
            return 'Missing username!'

        username = session['username'] = request.form['name']

        # Check for a file upload, we'll require this to compress ECG data
        if 'file' not in request.files:
            return 'Missing file!'
        file = request.files['file']

        # Validate file extension and process the file
        if file and validate_file_extensions.validate(file.filename):
            original_size = read_raw_file_size.get_file_size(file)
            samples = parse_ecg.read_samples(file)

            # Compress the ECG data here

            # Prepend the username to the filename
            filename = secure_filename(username+'_'+file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

            return (f'File {filename} uploaded successfully! '
                    f'<br> Original size: {original_size} bytes <br> '
                    f'<a href="/ecg/download/{filename}">Download</a>')

    if 'username' in session:
        print(f'Logged in as {session["username"]}')

    return render_template('compress.html')
