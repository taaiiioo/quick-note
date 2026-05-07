from flask import  Flask, request, render_template, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv 
import os
load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'

db = SQLAlchemy(app)  

class Note(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    content = db.Column(db.Text, nullable = False)
    date = db.Column(db.DateTime, default= datetime.utcnow)

    def __repr__(self):
        return f"<Note {self.id}>"
    
class Task(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    content = db.Column(db.Text, nullable = False)
    done = db.Column(db.Boolean, default= False)
    date = db.Column(db.DateTime, default= datetime.utcnow)

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80), nullable = False, unique = True)
    password = db.Column(db.String(200), nullable = False)
    


with app.app_context():
    db.create_all()


@app.route('/')
def home():
    if 'id' in session:
        return redirect('/notes')
    return redirect('/register')

@app.route('/notes', methods = ['POST' ,'GET'])
def add ():
    if 'id' not in session:
        return redirect ('/login')
    if request.method == 'POST':
        your_note = request.form['content']
        new_note = Note(content = your_note, user_id=session['id'])

        try:
            db.session.add(new_note)
            db.session.commit()
            return redirect('/notes')
        except:
            return "something went wrong "
        # return "you did it"
    else:
     notes = Note.query.filter_by(user_id=session['id']).order_by(Note.date.desc()).all()
     return render_template('index.html', notes=notes)
    

@app.route('/notes/delete',methods = ['POST'])
def delete ():
    if 'id' not in session:
        return redirect ('/login')
    note_id = request.form['id']
    delete_note = Note.query.get(note_id)
    if delete_note.user_id != session['id']:
        return redirect('/notes')

    try:
        db.session.delete(delete_note)
        db.session.commit()
        return redirect('/notes')
    except:
        return "there was a problem deleting your note..."
    
@app.route('/notes/update', methods=['POST', 'GET'])
def update():
    if 'id' not in session:
        return redirect ('/login')
    if request.method =='POST':
        note_id = request.form['id']
        update_note = Note.query.get(note_id)
        updated_note=request.form['content']
        if update_note.user_id != session['id']:
            return redirect('/notes')
        update_note.content = updated_note
        try:
            db.session.commit()
            return redirect('/notes')
        except:
            return "there was a problem updating your note"
    
    else:
        notes = Note.query.filter_by(user_id=session['id']).order_by(Note.date).all()
        return render_template('index.html', notes=notes)
    


@app.route('/tasks', methods= ['POST', 'GET'])
def add_task():
        if 'id' not in session:
            return redirect ('/login')

        if request.method == 'POST':
            your_task = request.form['content']
            new_task = Task(content = your_task, user_id=session['id'])

            try:
                db.session.add(new_task)
                db.session.commit()
                return redirect('/tasks')
            except:
                return "something went wrong "
                # return "you did it"
        else:
            tasks = Task.query.filter_by(user_id=session['id']).order_by(Task.date.desc()).all()
            return render_template('task.html', tasks=tasks)


@app.route('/tasks/delete',methods = ['POST'])
def delete_task ():
    if 'id' not in session:
        return redirect ('/login')
    task_id = request.form['id']
    task_to_delete = Task.query.get(task_id)
    if task_to_delete.user_id != session['id']:
        return redirect('/tasks')

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/tasks')
    except:
        return "there was a problem deleting your task..."
    

@app.route('/tasks/update', methods=['POST', 'GET'])
def update_task():
    if 'id' not in session:
        return redirect ('/login')
    if request.method =='POST':
        task_id = request.form['id']
        task_to_update = Task.query.get(task_id)
        updated_task=request.form['content']
        if task_to_update.user_id != session['id']:
            return redirect('/tasks')
        task_to_update.content = updated_task
        try:
            db.session.commit()
            return redirect('/tasks')
        except:
            return "there was a problem updating your task"
    
    else:
        tasks = Task.query.filter_by(user_id=session['id']).order_by(Task.date).all()
        return render_template('task.html', tasks=tasks)
    
@app.route('/tasks/toggle', methods=['POST'])
def task_toggle():
    if 'id' not in session:
        return redirect ('/login')
    task_id = request.form['id']
    task_to_done = Task.query.get(task_id)
    if task_to_done.user_id != session['id']:
        return redirect('/tasks')
    if task_to_done.done == False:
        task_to_done.done = True
    else:
        task_to_done.done = False
    
    try:
        db.session.commit()
        return redirect('/tasks')
    except:
        return "some issue found.."


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        name = request.form['username']
        password = request.form['password']
        user_to_check = User.query.filter_by(username=name).first()
        if user_to_check:
            flash('Username already exists! Please login.')
            return redirect('/login')
        else:
            hashed_password = generate_password_hash(password)
            new_user = User(username = name, password = hashed_password)
            try:
                db.session.add(new_user)
                db.session.commit()
                session['id'] = new_user.id
                return redirect('/notes')
            except:
                return "something went wronge your user is not registered..."
    else:
        return render_template('register.html')
    

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        password = request.form['password']
        user_to_check = User.query.filter_by(username=user).first()
        if user_to_check is None:
            return redirect('/register')
        else:
            confirming = check_password_hash(user_to_check.password, password)
        if confirming:
            session['id'] = user_to_check.id
            return redirect('/notes')
            
        else:
            flash('wrong password try again...')
            return redirect('/login')
        
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('id', None)
    return redirect('/login')

# @app.route('/', methods = ['POST' ,'GET'])
# def add ():
#     return render_template('index.html')
    # return "hello yo yo!"


if __name__ == "__main__":
    app.run(debug=True)