from flask import Flask
import os
from dotenv import load_dotenv
load_dotenv()


def create_app():
    """
    This is the main app factory function.
    :return:
    """
    # App configuration
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['UPLOAD_FOLDER'] = './uploads'
    app.config['ALLOWED_EXTENSIONS'] = {'bin'}

    print(app.config['SECRET_KEY'])

    # Register blueprint to handle ECG functionality
    from ecg import ecg_controller
    app.register_blueprint(ecg_controller.bp)

    # Register a root route
    @app.route('/')
    def index():
        return '<a href="/ecg">Upload ECG Data</a>'

    return app

