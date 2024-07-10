from flask import Flask, render_template, request, redirect, url_for
# from flask_sqlalchemy import SQLAlchemy
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
@app.route('/', methods=["POST","GET"])
def index():
    if request.method == 'POST':
        content = request.form["content"]
        status = request.form.get("status", "0")
        status = 1 if status == "on" else 0
        created_on = date.today().strftime("%d-%m-%y")
        with sqlite3.connect("database.db") as users:
            cursor = users.cursor()
            cursor.execute("INSERT INTO TODO (content, created_on, status)VALUES (?,?,?)", (content, created_on, status))
            users.commit()
        with sqlite3.connect("database.db") as users:
            cursor = users.cursor()
            cursor.execute("SELECT * FROM TODO")
            todos = cursor.fetchall()
        print("*************POST request sent******************")
        # return render_template("index.html")
        return render_template("index.html",todos=todos)
   
    else:
        print("*************GET request sent******************")
        with sqlite3.connect("database.db") as users:
            cursor = users.cursor()
            cursor.execute("SELECT * FROM TODO")
            todos = cursor.fetchall()
        # return render_template("index.html")
        print("*************GET request sent******************")
        return render_template("index.html",todos=todos)
    
@app.route('/delete/<int:entry_id>')
def delete_entry(entry_id):
    entry_id = int(entry_id)
    with sqlite3.connect("database.db") as users:
        cursor = users.cursor()
        cursor.execute("delete from TODO where id=?", (entry_id,))
        users.commit()
    return redirect('/')
   


if __name__ == "__main__":
    app.run(debug=True)
