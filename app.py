from flask import Flask, render_template, request, redirect, url_for
# from flask_sqlalchemy import SQLAlchemy
import sqlite3
from datetime import datetime

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
@app.route('/', methods=["POST","GET"])
def index():
    if request.method == 'POST':
        content = request.form['name']
        status = request.form['status']
        create_on = datetime.now.strftime("%Y-%m-%d %H:%M:%S")

        with sqlite3.connect("database.db") as users:
            cursor = users.cursor()
            cursor.execute("INSERT INTO TODO \ (content, create_on, status)VALUES (?,?,?)", (content, create_on, status))
            users.commit()
        # return render_template("index.html")
        return redirect(url_for('index'))
    else:
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM TODO")
            todos = cursor.fetchall()

        # return render_template("index.html")
        return render_template("index.html", todos=todos)

if __name__ == "__main__":
    app.run(debug=True)
