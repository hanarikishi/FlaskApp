from flask import Flask
from flask_cors import CORS
from flaskr import db
from flaskr.main import bp as main_bp

def create_app(test_config=None):
    app = Flask(__name__)
    CORS(app)

    app.config["DATABASE"] = "database.db"
    if test_config:
        app.config.update(test_config)

    # アプリコンテキスト内でテーブル作成
    with app.app_context():
        db.create_tasks_table()

    app.register_blueprint(main_bp)

    return app
