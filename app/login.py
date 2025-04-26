from flask import Flask, render_template, request, redirect, url_for, flash, session
from app import app
from app.config import get_db_connection


# Routes
@app.route('/')
def home():
    return render_template('home.html')


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

        cursor = None
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT * FROM Users WHERE username = %s', (username,))
            user = cursor.fetchone()
            
            if not user or user['password'] != password:
                flash('Invalid username or password', 'error')
                return redirect(url_for('login'))

            if user['email'] != email or user['urole'] != urole:
                flash('Invalid email or role', 'error')
                return redirect(url_for('login'))

            session['user_id'] = user['user_id']
            session['username'] = user['username']
            session['email'] = user['email']
            session['urole'] = user['urole']

            return redirect(url_for('home'))
        except Exception as e:
            flash(f'Error during login: {str(e)}', 'error')
            return redirect(url_for('login'))
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))
