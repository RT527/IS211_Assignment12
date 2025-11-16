# Rafi Talukder Assignment_12
import sqlite3
from flask import Flask, render_template, request, redirect, session, g, url_for
"""---------------------------------------------------------------------------------"""
app = Flask(__name__)
app.secret_key = "supersecretkey"
DATABASE = 'hw13.db'
"""---------------------------------------------------------------------------------"""
def get_db(): # Database helper
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(error):
    db = g.pop('db', None)
    if db is not None:
        db.close()
"""---------------------------------------------------------------------------------"""
def login_required(f): # Login
    def wrapper(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect('/login')
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == "admin" and password == "password":
            session['logged_in'] = True
            return redirect('/dashboard')
        else:
            error = "Invalid credentials"
            return render_template('login.html', error=error)
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')
"""---------------------------------------------------------------------------------"""
@app.route('/dashboard') # Dashboard
@login_required
def dashboard():
    db = get_db()
    students = db.execute("SELECT * FROM students").fetchall()
    quizzes = db.execute("SELECT * FROM quizzes").fetchall()
    return render_template('dashboard.html', students=students, quizzes=quizzes)
"""---------------------------------------------------------------------------------"""
@app.route('/student/add', methods=['GET', 'POST']) # Add Students
@login_required
def add_student():
    error = None
    if request.method == 'POST':
        first = request.form['first_name']
        last = request.form['last_name']
        if not first or not last:
            error = "All fields required"
            return render_template('add_student.html', error=error)
        db = get_db()
        db.execute("INSERT INTO students (first_name, last_name) VALUES (?, ?)",
                   (first, last))
        db.commit()
        return redirect('/dashboard')
    return render_template('add_student.html', error=error)
"""---------------------------------------------------------------------------------"""
@app.route('/quiz/add', methods=['GET', 'POST']) # Add Quiz
@login_required
def add_quiz():
    error = None
    if request.method == 'POST':
        subject = request.form['subject']
        num_questions = request.form['num_questions']
        quiz_date = request.form['quiz_date']
        if not subject or not num_questions or not quiz_date:
            error = "All fields required"
            return render_template('add_quiz.html', error=error)
        db = get_db()
        db.execute(
            "INSERT INTO quizzes (subject, num_questions, quiz_date) VALUES (?, ?, ?)",
            (subject, num_questions, quiz_date)
        )
        db.commit()
        return redirect('/dashboard')
    return render_template('add_quiz.html', error=error)
"""---------------------------------------------------------------------------------"""
# View Student Results

"""---------------------------------------------------------------------------------"""
# Add Result Score

"""---------------------------------------------------------------------------------"""
# Anonymous Quiz Results

"""---------------------------------------------------------------------------------"""
if __name__ == '__main__':
    app.run(debug=True)
