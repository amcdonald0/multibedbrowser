from flask import Flask, render_template, jsonify
from app import app
import mariadb
from app.config import get_db_connection


@app.route('/search')
def index():
    return render_template('search.html')


@app.route('/get_studies')
def get_studies():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT studyname FROM Studies")
    studies = [row[0] for row in cur.fetchall()]
    cur.close()
    conn.close()
    return jsonify(studies)

@app.route('/get_files/<studyname>')
def get_files(studyname):
    conn = get_db_connection()
    cur = conn.cursor()
    query = """
        SELECT f.file_name
        FROM Files f
        JOIN Studies s ON f.study_id = s.id
        WHERE s.studyname = %s
    """
    cur.execute(query, (studyname,))
    files = [row[0] for row in cur.fetchall()]
    cur.close()
    conn.close()
