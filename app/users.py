#!/usr/bin/env python3

from flask import render_template
from app import app
import mariadb

# Функция подключения к БД
def get_db_connection():
    return mariadb.connect(
        user='zhanna',
        password='Zhan',
        host='bioed-new.bu.edu',
        database='Team14',
        port=4253
    )

# Роут для страницы Users
@app.route('/users')
def show_users():
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Запрос к таблице Users
        cur.execute("SELECT id, username, password, email, role FROM Users")
        results = cur.fetchall()

        cur.close()
        conn.close()

        return render_template('users.html', results=results, resultsAllUsers="All users in the system")

    except mariadb.Error as e:
        print(f"Error connecting to MariaDB: {e}")
        return render_template('users.html', results=None, resultsAllUsers=None)
