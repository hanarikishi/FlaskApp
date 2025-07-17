from flask import Flask
from flaskr import db, main
from flask_cors import CORS

app =Flask(__name__)
CORS(app)
db.create_tasks_table()

# 今後こっちに移行するかも
# def create_app():
#     app = Flask(__name__)
#     CORS(app)
#     db.create_tasks_table()
#     return app