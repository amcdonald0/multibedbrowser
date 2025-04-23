#!/usr/bin/env python3

from flask import Flask, render_template, request, jsonify
from app import app
import json
import sys
import mariadb

def get_db_connection():
    # Update with your actual DB credentials
    conn =  mariadb.connect(
        user='aretham',
        password='WaitWell024!',
        host='bioed-new.bu.edu',
        database='Team14',
        port=4253 
    )

@app.route('/')
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
