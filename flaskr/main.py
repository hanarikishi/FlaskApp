from flaskr import app
from flask import render_template, request, redirect, url_for
import sqlite3
from flask import jsonify

DATABASE ="database.db"

def get_data():
    # DBから取得
    con = sqlite3.connect(DATABASE)

    #DBのtacksテーブルの全レコードを取得し、タプルのリストとして受け取る
    db_tasks = con.execute('SELECT * FROM tasks').fetchall()
    con.close()

    tasks = []
    for row in db_tasks:
        tasks.append({'id':row[0],'title':row[1], 'deadline':row[2], 'status':row[3], 'priority':row[4], 'tag':row[5],'memo':row[6]})
    return tasks

@app.route('/api/tasks', methods = ['GET'])
def api_get_tasks():
    tasks = get_data()
    return jsonify(tasks)

@app.route('/api/tasks', methods=['POST'])
def api_create_task():
    data     = request.get_json()
    title    = data.get('title')
    deadline = data.get('deadline')
    status   = data.get('status')
    priority = data.get('priority')
    tag      = data.get('tag')
    memo     = data.get('memo')
    
    con =sqlite3.connect(DATABASE)
    con.execute(
        'INSERT INTO tasks (title, deadline, status, priority, tag, memo) VALUES (?, ?, ?, ?, ?, ?)',
        (title, deadline, status, priority, tag, memo)
    )
    con.commit()
    con.close()
    return jsonify({'message': 'Task created successfully'}), 201

@app.route('/')
def index():
    
    tasks = get_data()
    return render_template(
        'index.html',
        tasks=tasks
        )
    
@app.route('/form')
def form():
    
    tasks = get_data()
    return render_template(
        'form.html',
        tasks=tasks
        )

@app.route('/register',methods=['POST'])
def register():
    title = request.form['title']
    deadline = request.form['deadline']
    status = request.form['status']
    priority = request.form['priority']
    tag = request.form['tag']
    memo = request.form['memo']
    delete_ids = request.form.getlist('delete_ids')

    con = sqlite3.connect(DATABASE)
    # 登録
    if title != "" and deadline != "" and status != "" and priority != "" :
        con.execute('INSERT INTO tasks (title, deadline, status, priority, tag, memo) VALUES(?,?,?,?,?,?)',
                    [title, deadline, status, priority, tag, memo])
    # 削除
    for i in delete_ids:
            con.execute('DELETE FROM tasks Where id = (?)',[i])

    con.commit()
    con.close()
    return redirect(url_for('index'))

# /detail/task_idのURLにする
@app.route('/detail/<int:task_id>')
def detail(task_id):
    con = sqlite3.connect(DATABASE)

    #(task_id,)のように「,」がないとタプルではなく単なる値を渡してしまう。
    db_task = con.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
    con.close()

    task = []
    if db_task:
        task = {'id': db_task[0], 'title': db_task[1], 'deadline': db_task[2],'status': db_task[3], 'priority': db_task[4], 'tag': db_task[5], 'memo': db_task[6]}
    else:
        task = None
    return render_template(
        'detail.html',
        task = task
    )
