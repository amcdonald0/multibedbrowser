from flask import Flask, render_template, request, redirect, url_for, flash, session
import mariadb
from app import app

# Create Flask application
def get_db_connection():
    try:
        conn = mariadb.connect(
            user='zhanna',
            password='Zhan',
            host='bioed-new.bu.edu',
            database='Team14'
        )
        conn.row_factory = mariadb.Row  # Optional, for dict-like access to rows
        return conn
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB: {e}")
        return None
# Routes
@app.route('/')
# @login_required
def home():
    return render_template('templates/login.html')

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
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM Users WHERE username = ?', (username,))
            user = cursor.fetchone()
            
            if not user or user[3] != password:  # adjust index if not using row_factory
                flash('Invalid username or password', 'error')
                return redirect(url_for('login'))

            if user[2] != email or user[4] != urole:
                flash('Invalid email or role', 'error')
                return redirect(url_for('login'))

            session['user_id'] = user[0]
            session['username'] = user[1]
            session['email'] = user[2]
            session['urole'] = user[4]

            return redirect(url_for('home'))
        finally:
            cursor.close()
            conn.close()

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# Import other routes
# from routes import *
