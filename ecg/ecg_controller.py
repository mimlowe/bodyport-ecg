from flask import Blueprint, request, render_template, current_app, session
from werkzeug.utils import secure_filename
from utils import validate_file_extensions, read_raw_file_size
from ecg import parse_ecg
import os

bp = Blueprint('ecg', __name__, url_prefix='/ecg')


@bp.route('/download/<filename>')
def download_file(filename):
    username = session.get('username', None)
    username = secure_filename(username)
    if username is not None and os.path.isdir(f'{current_app.config['UPLOAD_FOLDER']}/{username}/'):
        samples = parse_ecg.read_24bit_samples(f'{current_app.config['UPLOAD_FOLDER']}/{username}/{filename}')

        # Remove the file after reading it
        os.remove(f'{current_app.config['UPLOAD_FOLDER']}/{username}/{filename}')

        # If the directory associated with this user contains no files, delete the directory
        if not os.listdir(f'{current_app.config['UPLOAD_FOLDER']}/{username}/'):
            os.rmdir(f'{current_app.config['UPLOAD_FOLDER']}/{username}/')

        return samples
    return 'File not found!'


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

            # Compress the ECG data here

            # We need to sanitize the filename and username before using them to modify the filesystem
            filename = secure_filename(file.filename)
            username = secure_filename(username)

            # We want to check if there exists an upload subdirectory for this session's user
            # If no path exists, we'll create it
            os.path.isdir(f'{current_app.config['UPLOAD_FOLDER']}/{username}/') or os.makedirs(
                f'{current_app.config['UPLOAD_FOLDER']}/{username}/')

            file.save(os.path.join(f'{current_app.config['UPLOAD_FOLDER']}/{username}/', filename))

            return (f'File {filename} uploaded successfully! '
                    f'<br> Original size: {original_size} bytes <br> '
                    f'<a href="/ecg/download/{filename}">Download {filename}</a>')

    if 'username' in session:
        print(f'Logged in as {session["username"]}')

    return render_template('compress.html', username=session.get('username', None))
