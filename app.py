from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import date

app = Flask(__name__)

connect = sqlite3.connect("database.db")
connect.execute(
    '''
    CREATE TABLE IF NOT EXISTS TODO (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    content TEXT, 
    created_on TEXT, 
    status INTEGER
    )'''
)
connect.close()

@app.route('/', methods=["POST", "GET"])
def index():
    if request.method == 'POST':
        content = request.form["content"]
        created_on = date.today().strftime("%d-%m-%y")
        with sqlite3.connect("database.db") as users:
            cursor = users.cursor()
            cursor.execute("INSERT INTO TODO (content, created_on, status) VALUES (?, ?, ?)", (content, created_on, 0))
            users.commit()
        return redirect(url_for('index'))

    else:
        with sqlite3.connect("database.db") as users:
            cursor = users.cursor()
            cursor.execute("SELECT * FROM TODO")
            todos = cursor.fetchall()
        return render_template("index.html", todos=todos)

@app.route('/delete/<int:entry_id>')
def delete_entry(entry_id):
    with sqlite3.connect("database.db") as users:
        cursor = users.cursor()
        cursor.execute("DELETE FROM TODO WHERE id=?", (entry_id,))
        users.commit()
    return redirect('/')

@app.route('/mark_as_done/<int:entry_id>')
def mark_as_done(entry_id):
    with sqlite3.connect("database.db") as users:
        cursor = users.cursor()
        cursor.execute("UPDATE TODO SET status = 1 WHERE id=?", (entry_id,))
        users.commit()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
