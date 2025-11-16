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
# Add Students

"""---------------------------------------------------------------------------------"""
# Add Quiz

"""---------------------------------------------------------------------------------"""
# View Student Results

"""---------------------------------------------------------------------------------"""
# Add Result Score

"""---------------------------------------------------------------------------------"""
# Anonymous Quiz Results

"""---------------------------------------------------------------------------------"""
if __name__ == '__main__':
    app.run(debug=True)
