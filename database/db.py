# FlaskアプリがSQLAlchemyを使えるようにするための初期化
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_db(app):
    db.init_app(app)