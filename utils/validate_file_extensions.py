from flask import current_app


def validate(filename):
    """
    This function validates the extension of a file name, checking if the current Flask app allows it.
    :param filename: String name of file to validate
    :return: Boolean
    """
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']
