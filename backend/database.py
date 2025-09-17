from flask_sqlalchemy import SQLAlchemy
from .config_database import ConfigDataDase

db = SQLAlchemy()


def init_db(app):
    app.config.from_object(ConfigDataDase)
    db.init_app(app)
    with app.app_context():
        db.create_all()
