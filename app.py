from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuring the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    complete = db.Column(db.Boolean, default=False)

# Home route to display tasks
@app.route('/')
def index():
    todo_list = Todo.query.all()
    return render_template('index.html', todo_list=todo_list)

# Add a new task
@app.route('/add', methods=['POST'])
def add():
    title = request.form.get('title')
    new_task = Todo(title=title)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('index'))

# Mark a task as complete
@app.route('/complete/<int:task_id>')
def complete(task_id):
    task = Todo.query.filter_by(id=task_id).first()
    task.complete = not task.complete
    db.session.commit()
    return redirect(url_for('index'))

# Delete a task
@app.route('/delete/<int:task_id>')
def delete(task_id):
    task = Todo.query.filter_by(id=task_id).first()
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))

# Update a task
@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit(task_id):
    task = Todo.query.filter_by(id=task_id).first()
    if request.method == 'POST':
        task.title = request.form['title']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', task=task)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables
    app.run(debug=True)

