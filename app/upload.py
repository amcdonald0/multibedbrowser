
from flask import Flask, render_template, request
import sys
import mariadb
from app import app

def get_db_connection():
    try:
        conn = mariadb.connect(
            user='jriya186',
            password='mushky1864',
            host='bioed-new.bu.edu',
            database='Team14', 
            port=4253
        )
        conn.row_factory = mariadb.Row  # Optional, for dict-like access to rows
        return conn
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB: {e}")
        return None
    
@app.route('/')
def home():
    return render_template("upload.html")

@app.route('/get_studies', method = "post")
def studies():
    study_name = request.args.get("studyname","").strip()
    file_name = request.args.get("file_name","").strip()
    file_path = request.args.get("final_filepath","").strip()
    #file_type = request.args.get("file_size","").strip()
    upload_date = request.args.get("upload_date","").strip() # use json timestamp function
    description = request.args.get("description","").strip()
    study_id = request.args.get("study_id","").strip()
    species = request.args.get("species","").strip()
    genome_release = request.args.get("genome_release","").strip()
    experiment_type = request.args.get("experiment_type","").strip()
    conn = get_db_connection()
    cur = conn.cursor()

    # Fetch projects
    query1 = """SELECT project_name FROM Projects"""
    cur.execute(query1)
    projects = cur.fetchall()

    # Fetch studies
    query2 = """SELECT study_name FROM Studies"""
    cur.execute(query2)
    studies = cur.fetchall()

    # insert file
    query3 = """SELECT study_id WHERE study_name = %s"""
    cur.execute(query3,[study_name])

    query4 = """
    INSERT INTO files (file_name, file_path, file_size, upload_date, description, study_id, species, genome_release, experiment_type)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    cur.execute(query4,[file_name,file_path, file_size, upload_date, description, study_id, species, genome_release, experiment_type])
    conn.close()

    return render_template('upload.html', projects=projects, studies=studies)

if __name__ == '__main__':
    app.run(debug=True)