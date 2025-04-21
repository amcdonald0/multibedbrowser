from flask import Flask, render_template, request, redirect, url_for, flash, session
import mariadb
from app import app

# Create Flask application
def login_required(f):
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

# Routes
@app.route('/')
# @login_required
def home():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        urole = request.form.get('urole')

        if not all([username, email, password, urole]):
            flash('All fields are required', 'error')
            return redirect(url_for('login'))

        conn = get_db_connection()
        if not conn:
            flash('Database connection error', 'error')
            return redirect(url_for('login'))

        try:
            with conn.cursor() as cursor:
                cursor.execute('SELECT * FROM Users WHERE username = %s', (username,))
                user = cursor.fetchone()
                
                if not user or user['password'] != password:
                    flash('Invalid username or password', 'error')
                    return redirect(url_for('login'))

                if user['email'] != email or user['urole'] != urole:
                    flash('Invalid email or role', 'error')
                    return redirect(url_for('login'))

                # Сохраняем информацию о пользователе в сессии
                session['user_id'] = user['user_id']
                session['username'] = user['username']
                session['email'] = user['email']
                session['urole'] = user['urole']
                
                return redirect(url_for('home'))
        finally:
            conn.close()

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('login'))

# Import other routes
# from routes import *
