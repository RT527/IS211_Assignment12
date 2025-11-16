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
@app.route('/student/<int:id>') # View Student Results
@login_required
def student_results(id):
    db = get_db()
    student = db.execute("SELECT * FROM students WHERE id=?", (id,)).fetchone()
    results = db.execute("""
        SELECT results.score, results.quiz_id, quizzes.subject, quizzes.quiz_date
        FROM results
        JOIN quizzes ON quizzes.id = results.quiz_id
        WHERE results.student_id=?
    """, (id,)).fetchall()
    return render_template("student_results.html",
                           student=student,
                           results=results)
"""---------------------------------------------------------------------------------"""
@app.route('/results/add', methods=['GET', 'POST']) # Add Result Score
@login_required
def add_result():
    db = get_db()
    students = db.execute("SELECT * FROM students").fetchall()
    quizzes = db.execute("SELECT * FROM quizzes").fetchall()
    error = None
    if request.method == 'POST':
        student_id = request.form['student_id']
        quiz_id = request.form['quiz_id']
        score = request.form['score']
        if not student_id or not quiz_id or not score:
            error = "All fields required"
            return render_template('add_result.html', students=students, quizzes=quizzes, error=error)
        db.execute("INSERT INTO results (student_id, quiz_id, score) VALUES (?, ?, ?)",
                   (student_id, quiz_id, score))
        db.commit()
        return redirect('/dashboard')
    return render_template("add_result.html",
                           students=students,
                           quizzes=quizzes,
                           error=error)
"""---------------------------------------------------------------------------------"""
@app.route('/quiz/<int:id>/results/') # Anonymous Quiz Results
def quiz_results_anon(id):
    db = get_db()
    quiz = db.execute("SELECT * FROM quizzes WHERE id=?", (id,)).fetchone()
    results = db.execute("""
        SELECT student_id, score 
        FROM results
        WHERE quiz_id=?
    """, (id,)).fetchall()
    return render_template('quiz_results_anon.html',
                           quiz=quiz,
                           results=results)
"""---------------------------------------------------------------------------------"""
if __name__ == '__main__':
    app.run(debug=True)
