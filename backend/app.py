from flask import Flask
from flask_cors import CORS
from backend.database import db
from backend.routes import faq_bp


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/gilunix/Documents/Projects/chatbot_gsantana/backend/database/gsantana.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    from backend.models import FAQ
    with app.app_context():
        db.create_all()

    app.register_blueprint(faq_bp)
    @app.route('/')
    def index():
        return 'API do Chatbot Gsantana está online'
    return app

if __name__=='__main__':
    app = create_app()
    app.run(host='0.0.0.0',port=5000)


