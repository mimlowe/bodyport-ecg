from flask import Blueprint, request, render_template, current_app, session, send_file
from werkzeug.utils import secure_filename
from utils import validate_file_extensions
from ecg.compression.compress_ecg import compress_file
import os

bp = Blueprint('ecg', __name__, url_prefix='/ecg')


@bp.route('/download/<filename>')
def download_file(filename):
    """
    Endpoint to download a compressed file
    :param filename:
    :return:
    """

    # Retrieve the username from the session, we need to use this to locate the file
    username = session.get('username', None)

    # Check if the username is valid and if the path exists
    if username is not None and os.path.isdir(f'{current_app.config['UPLOAD_FOLDER']}/{username}/'):

        # Send the file
        return send_file(f'{current_app.config['UPLOAD_FOLDER']}/{username}/{filename}',
                         as_attachment=True, download_name="compressed.bin")

    return 'File not found!'


@bp.route('/compress/<filename>', methods=['POST'])
def compress(filename):
    """
    Endpoint to compress an uploaded file
    :param filename:
    :return:
    """

    # Retrieve the username from the session, we need to use this to locate the file
    username = session.get('username', None)

    # Check if the username is valid and if the path exists
    if username is not None and os.path.isdir(f'{current_app.config['UPLOAD_FOLDER']}/{username}/'):

        compressed_path = f'{current_app.config['UPLOAD_FOLDER']}/{username}/{filename}'

        # Perform the compression and retrieve metadata
        metadata = compress_file(compressed_path, compressed_path)

        return (f'File {filename} compressed successfully! <br><hr>'
                f'{metadata}<br><hr>'
                f'<a href="/ecg/download/{filename}">Download compressed file</a>')

    return 'File not found!'


@bp.route('/', methods=['GET', 'POST'])
def upload_file():
    """
    Endpoint to upload and compress ECG data
    :return:
    """
    if request.method == 'POST':

        # Check for username field, we'll use it to set a session variable.
        # We may use session variables to identify the user's files when performing the download.
        if 'name' not in request.form:
            return 'Missing username!'

        username = session['username'] = secure_filename(request.form['name'])

        # Check for a file upload, we'll require this to compress ECG data
        if 'file' not in request.files:
            return 'Missing file!'
        file = request.files['file']

        # Validate file extension and process the file
        if file and validate_file_extensions.validate(file.filename):

            # We need to sanitize the filename and username before using them to modify the filesystem
            filename = secure_filename(file.filename)
            # username = secure_filename(username)

            # We want to check if there exists an upload subdirectory for this session's user
            # If no path exists, we'll create it
            os.path.isdir(f'{current_app.config['UPLOAD_FOLDER']}/{username}/') or os.makedirs(
                f'{current_app.config['UPLOAD_FOLDER']}/{username}/')

            # Save the file in the user's directory, we'll later overwrite the file with the compressed data
            file.save(os.path.join(f'{current_app.config['UPLOAD_FOLDER']}/{username}/', filename))

            # Render the compress template with the username and filename
            return render_template('compress.html',
                                   username=session.get('username', ''),
                                   filename=filename,
                                   url=f'/ecg/compress/{filename}')

    return render_template('upload.html', username=session.get('username', ''))
