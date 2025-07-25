import sqlite3
from flask import current_app

DATABASE = "database.db"

def get_connection():
    db_path = current_app.config.get("DATABASE", DATABASE)
    return sqlite3.connect(db_path)

def create_tasks_table():
    con = get_connection()
    con.execute('''
        CREATE TABLE IF NOT EXISTS tasks(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            status TEXT,
            priority TEXT,
            tag TEXT,
            start TEXT,
            deadline TEXT,
            memo TEXT
        )
    ''')
    con.close()
