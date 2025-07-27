from flaskr import db
from flaskr import create_app


def test_get_connection():
    app = create_app()
    with app.app_context():
        con = db.get_connection()
        assert con is not None
        con.close()

def test_create_tasks_table():
    app = create_app()
    with app.app_context():
        db.create_tasks_table()

        con = db.get_connection()
        cursor = con.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='tasks'")
        table_exists = cursor.fetchone() is not None
        con.close()

        assert table_exists
