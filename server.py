from flask import Flask


def create_app():
    # App configuration
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = './uploads'
    app.config['ALLOWED_EXTENSIONS'] = {'bin'}

    # Register blueprint to handle ECG functionality
    from ecg import ecg_controller
    app.register_blueprint(ecg_controller.bp)

    # Register a root route
    @app.route('/')
    def index():
        return '<a href="/ecg">Upload ECG Data</a>'

    return app

