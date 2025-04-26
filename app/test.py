from flask import Flask, render_template
import mariadb

app = Flask(__name__)


def get_db_connection():
    try:
        conn = mariadb.connect(
            user='jriya186',
            password='mushky1864',
            host='bioed-new.bu.edu',
            database='Team14',
            port=4253
        )
        return conn
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB: {e}")
        return None
    
@app.route('/test')
def show():
    return render_template("test.html")

# Routing: Display project name and research name
@app.route('/studies', methods=['GET'])
def studies():
    conn = get_db_connection()
    if not conn:
        return "Database connection failed", 500

    try:
        cur = conn.cursor()
        
        # query Projects table
        cur.execute("SELECT project_name FROM Projects")
        projects = cur.fetchall()  # get bname
        
        # query Studies table
        cur.execute("SELECT study_name FROM Studies")
        studies = cur.fetchall()  # 
        
    except mariadb.Error as e:
        print(f"Database error: {e}")
        return "Database operation failed", 500
    finally:
        conn.close()

    # Passing data to the front-end template
    return render_template('test.html', projects=projects, studies=studies)

if __name__ == '__main__':
    app.run(debug=True)