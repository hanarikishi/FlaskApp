from flask import Blueprint, request, render_template, jsonify, redirect, url_for
import sqlite3
from flaskr.db import get_connection

bp = Blueprint('main', __name__)

def get_data():
    # DBから取得
    con = get_connection()

    #DBのtacksテーブルの全レコードを取得し、タプルのリストとして受け取る
    db_tasks = con.execute('SELECT * FROM tasks').fetchall()
    con.close()

    tasks = []
    for row in db_tasks:
        tasks.append({'id':row[0],'title':row[1], 'status':row[2], 'priority':row[3], 'tag':row[4], 'start':row[5], 'deadline':row[6],'memo':row[7]})
    return tasks

@bp.route('/api/tasks', methods = ['GET'])
def api_get_tasks():
    tasks = get_data()
    return jsonify(tasks)

@bp.route('/api/tasks', methods=['POST'])
def api_create_task():
    data     = request.get_json()
    title    = data.get('title')
    status   = data.get('status')
    priority = data.get('priority')
    tag      = data.get('tag')
    start    = data.get('start')
    deadline = data.get('deadline')
    memo     = data.get('memo')

    con = get_connection()
    con.execute(
        'INSERT INTO tasks (title, status, priority, tag, start, deadline, memo) VALUES (?, ?, ?, ?, ?, ?, ?)',
        (title, status, priority, tag, start, deadline, memo)
    )
    con.commit()
    con.close()
    return jsonify({'message': 'Task created successfully'}), 201

@bp.route('/api/tasks/<int:task_id>', methods = ['PUT'])
def api_update_task(task_id):
    data     = request.get_json()
    title    = data.get('title')
    status   = data.get('status')
    priority = data.get('priority')
    tag      = data.get('tag')
    start    = data.get('start')
    deadline = data.get('deadline')
    memo     = data.get('memo')

    con = get_connection()
    con.execute(
        'UPDATE tasks SET title=?, status=?, priority=?, tag=?, start=?, deadline=?, memo=? WHERE id=?',
        (title, status, priority, tag, start, deadline, memo, task_id)
    )
    con.commit()
    con.close()
    return jsonify({'message': 'Task updated successfully'}), 200

@bp.route('/api/tasks/<int:task_id>', methods = ['DELETE'])
def api_task_delete(task_id):

    con = get_connection()
    con.execute(
        'DELETE FROM tasks WHERE id=?', (task_id,)
    )
    con.commit()
    con.close()
    return jsonify({'message': 'Task deleted successfully'}),200

@bp.route('/')
def index():

    tasks = get_data()
    return render_template(
        'index.html',
        tasks=tasks
        )

@bp.route('/form')
def form():

    tasks = get_data()
    return render_template(
        'form.html',
        tasks=tasks
        )

@bp.route('/register',methods=['POST'])
def register():
    title = request.form['title']
    status = request.form['status']
    priority = request.form['priority']
    tag = request.form['tag']
    start = request.form['start']
    deadline = request.form['deadline']
    memo = request.form['memo']
    delete_ids = request.form.getlist('delete_ids')

    con = get_connection()
    # 登録
    if title != "" and start != "" and deadline != "" and status != "" and priority != "" :
        con.execute('INSERT INTO tasks (title, status, priority, tag, start, deadline, memo) VALUES(?,?,?,?,?,?,?)',
                    [title, status, priority, tag, start, deadline, memo])
    # 削除
    for i in delete_ids:
            con.execute('DELETE FROM tasks Where id = (?)',[i])

    con.commit()
    con.close()
    return redirect(url_for('index'))

# /detail/task_idのURLにする
@bp.route('/detail/<int:task_id>')
def detail(task_id):
    con = get_connection()

    #(task_id,)のように「,」がないとタプルではなく単なる値を渡してしまう。
    db_task = con.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
    con.close()

    task = []
    if db_task:
        task = {'id': db_task[0], 'title': db_task[1], 'status': db_task[2], 'priority': db_task[3], 'tag': db_task[4], 'start': db_task[5], 'deadline': db_task[6],'memo': db_task[7]}
    else:
        task = None
    return render_template(
        'detail.html',
        task = task
    )
