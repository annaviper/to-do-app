from flask import Flask, render_template, redirect, request
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

Scss(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    created = db.Column(db.DateTime, default=datetime.now)
    done = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Task {self.id}>'
    
with app.app_context():
        db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index() -> str:
    # Add a task
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Task(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            error_msg = "Error: {e}"
            print(error_msg)
            return error_msg
    else: 
        # See all current tasks
        tasks = Task.query.order_by(Task.created).all()
        return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:task_id>')
def delete(task_id: int) -> str:
    task_to_delete = Task.query.get_or_404(task_id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except Exception as e:
        error_msg = "Error: {e}"
        print(error_msg)
        return error_msg

@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit(task_id: int) -> str:        
    task_to_update = Task.query.get_or_404(task_id)

    if request.method == 'POST':
        task_to_update.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except Exception as e:
            error_msg = "Error: {e}"
            print(error_msg)
            return error_msg
    else:
        return render_template('edit.html', task=task_to_update)

@app.route('/done/<int:task_id>')
def done(task_id: int) -> str:
    task_to_update = Task.query.get_or_404(task_id)

    try:
        task_to_update.done = not task_to_update.done
        db.session.commit()
        return redirect('/')
    except Exception as e:
        error_msg = "Error: {e}"
        print(error_msg)
        return error_msg
    

if __name__ == '__main__':
    app.run(port=8000, debug=True)