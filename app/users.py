from flask import render_template, flash
from app import app
import mariadb
from app.config import get_db_connection


@app.route('/users')
def show_users():
    try:
        conn = get_db_connection()
        if conn is None:
            flash('Ошибка подключения к базе данных', 'error')
            return render_template('users.html', results=None, resultsAllUsers=None)
            
        cur = conn.cursor(dictionary=True)

        cur.execute("SELECT user_id, username, email, urole FROM Users")
        results = cur.fetchall()

        cur.close()
        conn.close()

        return render_template('users.html', results=results, resultsAllUsers="All users in the system")

    except mariadb.Error as e:
        print(f"Error connecting to MariaDB: {e}")
        flash(f'Ошибка базы данных: {str(e)}', 'error')
        return render_template('users.html', results=None, resultsAllUsers=None)
