from flask import Flask
from flask_cors import CORS
from .database import init_db
from .routes import faq_bp


def create_app():
    app = Flask(__name__)
    CORS(app)
    init_db(app)
    app.register_blueprint(faq_bp)

    @app.route('/')
    def index():
        return 'API do Chatbot Gsantana está online'

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000)
