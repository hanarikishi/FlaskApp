import sqlite3

DATABASE = "database.db"

def create_tasks_table():
    # コネクションオブジェクト(DBアクセス)
    con = sqlite3.connect(DATABASE)
    
    # SQL文を実行するためのメソッド
    con.execute('''
                CREATE TABLE IF NOT EXISTS tasks(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                status TEXT,
                priority TEXT,
                tag TEXT,
                start TEXT,
                deadline TEXT,
                memo TEXT)
                ''')
    con.close()