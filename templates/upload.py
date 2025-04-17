
from flask import Flask, render_template, request
#import json
import mariadb

app = Flask(__name__)

# Connect to MariaDB
def get_db_connection():
    conn = mariadb.connect(
        user='jriya186',
        password='mushky1864',
        host='bioed-new.bu.edu',
        database='Team14'
    )
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()

    # Fetch projects
    cur.execute("SELECT project_id, project_name FROM Projects")
    projects = cur.fetchall()

    # Fetch studies
    cur.execute("SELECT study_id, stduy_name FROM Studies")
    studies = cur.fetchall()

    conn.close()

    return render_template('upload.html', projects=projects, studies=studies)

if __name__ == '__main__':
    app.run(debug=True)