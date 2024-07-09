from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  
db = SQLAlchemy(app)

class TODO(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500), nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.now)
    status = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<task %r>' % self.id

@app.route('/', methods=["POST","GET"])
def index():
    if request.method == "POST":
        task_content = request.form['content']
        print(task_content)
        new_task_content = TODO(content=task_content)
        
        task_status = request.form["status"]
        new_task_status = TODO(status=task_status)

        try:
            db.session.add(new_task_content)
            db.session.add(new_task_status)
            db.session.commit()
            return redirect('/')
        except:
            return 'error'

    else:
        tasks = TODO.query.order_by(TODO.created_on).all()
        return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
