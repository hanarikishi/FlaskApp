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
                deadline TEXT,
                status TEXT,
                priority TEXT,
                tag TEXT)
                ''')
    con.close()