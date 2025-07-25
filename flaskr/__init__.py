from flask import Flask
from flask_cors import CORS
from flaskr import db
from flaskr.main import bp as main_bp

def create_app():
    app = Flask(__name__)
    CORS(app)

    # 設定に DATABASE を追加（任意）
    app.config["DATABASE"] = "database.db"

    # アプリコンテキスト内でテーブル作成
    with app.app_context():
        db.create_tasks_table()

    app.register_blueprint(main_bp)

    return app
