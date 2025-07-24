from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
import mariadb
import os
from werkzeug.utils import secure_filename
import csv
import pandas as pd
from functools import wraps
import sqlite3
from datetime import datetime, timedelta
import subprocess

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # use for session encryption

# Session configuration
app.config.update(
    SESSION_COOKIE_SECURE=False,  # if not HTTPS, set to False
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
    SESSION_COOKIE_PATH='/students_25/Team14/app_test/test3',  # set cookie path
    PERMANENT_SESSION_LIFETIME=timedelta(minutes=60)  # session expiration time
)

app.config['APPLICATION_ROOT'] = '/students_25/Team14/app_test/test3'  # modify application root path
UPLOAD_FOLDER = "/var/www/html/students_25/Team14/app_test"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def get_db_connection():
    try:
        conn = mariadb.connect(
            user='YOUR_USERNAME',
            password='YOUR_PASSWORD!',
            host='HOST_NETWORK',
            port=1234,
            database='DATABASE/FILENAME i.e. Team14'
        )
        return conn
    except mariadb.Error as e:
        print(f"Database connection error: {e}")
        return None

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or not session.get('user_id'):
            flash('please login first')
            return redirect(url_for('login', _external=True))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
@app.route('/login')
def index():
    if 'user_id' in session:
        return redirect(url_for('home_page', _external=True))
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('home_page', _external=True))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        print(f"try to login: username={username}")
        
        try:
            conn = get_db_connection()
            if not conn:
                print("database connection failed")
                return render_template('login.html', error='database connection failed')
                
            cursor = conn.cursor()
            print("execute query...")
            cursor.execute('SELECT user_id, username, password, email, urole FROM Users WHERE username = %s', (username,))
            user = cursor.fetchone()
            
            print(f"query result: {user}")
            
            if user and password == user[2]:  # if user exists and password matches
                # set all necessary session variables
                session.clear()  # clear old session data
                session['user_id'] = user[0]
                session['username'] = user[1]
                session['urole'] = user[4] if user[4] is not None else 'guest'
                session['logged_in'] = True
                print(f"login successfully: urole={session['urole']}")
                flash('login successfully!')
                print("redirect to home_page")
                return redirect(url_for('home_page', _external=True))
            else:
                return render_template('login.html', error='username or password error')
                
        except Exception as e:
            print(f"login error: {e}")
            return render_template('login.html', error='login failed, please try again later')
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals() and conn:
                conn.close()
                
    return render_template('login.html')

@app.route('/test3/logout')
def logout():
    session.clear()
    return redirect(url_for('login', _external=True))

@app.route('/test3/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        email = request.form.get('email')

        # verify if password matches
        if password != confirm_password:
            return render_template('register.html', error="password does not match")

        # verify if password length is at least 8 characters
        if len(password) < 8:
            return render_template('register.html', error="password must be at least 8 characters")

        # verify if password contains letters and numbers
        if not any(c.isalpha() for c in password) or not any(c.isdigit() for c in password):
            return render_template('register.html', error="password must contain letters and numbers")

        conn = get_db_connection()
        if not conn:
            return render_template('register.html', error="database connection failed")
        try:
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM Users WHERE username = %s", (username,))
            if cur.fetchone()[0] > 0:
                return render_template('register.html', error="username already exists")
            cur.execute("SELECT COUNT(*) FROM Users WHERE email = %s", (email,))
            if cur.fetchone()[0] > 0:
                return render_template('register.html', error="email already exists")

            # insert new user
            cur.execute("""
                INSERT INTO PendingUsers (username, password, email, urole) 
                VALUES (%s, %s, %s, 'guest')
            """, (username, password, email))
            conn.commit()

            # get the ID of the newly inserted user
            cur.execute("SELECT pending_id FROM PendingUsers WHERE username = %s", (username,))
            user_id = cur.fetchone()[0]

            # set session
            session['user_id'] = user_id
            session['username'] = username
            session['urole'] = 'guest'

            flash('register successfully!')
            return redirect(url_for('home_page', _external=True))
        except Exception as e:
            print(f"register error: {e}")
            return render_template('register.html', error="register failed")
        finally:
            if conn:
                conn.close()
    return render_template('register.html')

@app.route('/test3/upload', methods=['GET', 'POST'])
@login_required
def upload_page():
    conn = get_db_connection()
    cur = conn.cursor()
    # Get all projects and studies for dropdowns
    cur.execute("SELECT project_id, project_name FROM Projects ORDER BY project_name")
    projects = cur.fetchall()
    cur.execute("SELECT study_id, study_name, project_id FROM Studies ORDER BY study_name")
    studies = cur.fetchall()
    cur.execute("SELECT user_id, username FROM Users WHERE urole IN ('admin', 'user') ORDER BY username")
    users = cur.fetchall()
    cur.execute("SELECT DISTINCT species FROM Files WHERE species IS NOT NULL AND species != ''")
    species_list = [row[0] for row in cur.fetchall()]
    cur.execute("SELECT DISTINCT genome_release FROM Files WHERE genome_release IS NOT NULL AND genome_release != ''")
    genome_release_list = [row[0] for row in cur.fetchall()]
    cur.execute("SELECT DISTINCT experiment_type FROM Files WHERE experiment_type IS NOT NULL AND experiment_type != ''")
    experiment_type_list = [row[0] for row in cur.fetchall()]
    error = None
    success = None

    if request.method == 'POST':
        project_id = request.form.get('project_id')
        new_project_name = request.form.get('new_project_name', '').strip()
        project_description = request.form.get('project_description', '').strip()
        study_id = request.form.get('study_id')
        new_study_name = request.form.get('new_study_name', '').strip()
        study_description = request.form.get('study_description', '').strip()

        # Check if project name exists
        if new_project_name:
            cur.execute("SELECT COUNT(*) FROM Projects WHERE project_name = %s", (new_project_name,))
            if cur.fetchone()[0] > 0:
                error = f"Project name '{new_project_name}' already exists, please use another name"
                conn.close()
                return render_template('upload.html',
                                    projects=projects,
                                    studies=studies,
                                    users=users,
                                    species_list=species_list,
                                    genome_release_list=genome_release_list,
                                    experiment_type_list=experiment_type_list,
                                    error=error,
                                    success=success)

        # Check if study name exists
        if new_study_name:
            cur.execute("SELECT COUNT(*) FROM Studies WHERE study_name = %s", (new_study_name,))
            if cur.fetchone()[0] > 0:
                error = f"Study name '{new_study_name}' already exists, please use another name"
                conn.close()
                return render_template('upload.html',
                                    projects=projects,
                                    studies=studies,
                                    users=users,
                                    species_list=species_list,
                                    genome_release_list=genome_release_list,
                                    experiment_type_list=experiment_type_list,
                                    error=error,
                                    success=success)

        # File upload part
        file = request.files.get('file')
        file_name = request.form.get('file_name', '').strip()
        
        # Check if file name exists
        if file_name:
            cur.execute("SELECT COUNT(*) FROM Files WHERE file_name = %s", (file_name,))
            if cur.fetchone()[0] > 0:
                error = f"File name '{file_name}' already exists, please use another name"
                conn.close()
                return render_template('upload.html',
                                    projects=projects,
                                    studies=studies,
                                    users=users,
                                    species_list=species_list,
                                    genome_release_list=genome_release_list,
                                    experiment_type_list=experiment_type_list,
                                    error=error,
                                    success=success)

        if not file:
            error = "No file uploaded"
        else:
            try:
                # deal with new project and study
                # 1. create new project
                if new_project_name:
                    pi_user_id = request.form.get('PI_id', '').strip()
                    cur.execute("INSERT INTO Projects (project_name, description) VALUES (%s, %s)", (new_project_name, project_description))
                    conn.commit()
                    project_id = cur.lastrowid
                    if pi_user_id:
                        cur.execute("INSERT INTO users_in (user_id, project_id) VALUES (%s,%s)",(pi_user_id,project_id))
                        conn.commit()
                # otherwise use the selected project
                # note: project_id must have a value

                # 2. create new study
                if new_study_name:
                    cur.execute("INSERT INTO Studies (study_name, description, project_id) VALUES (%s, %s, %s)", (new_study_name, study_description, project_id))
                    conn.commit()
                    study_id = cur.lastrowid
                # otherwise use the selected study
                # note: study_id must have a value

                # 3. use project_id and study_id to get names
                cur.execute("SELECT project_name FROM Projects WHERE project_id = %s", (project_id,))
                project_row = cur.fetchone()
                if not project_row:
                    raise Exception(f"Project id {project_id} not found in database")
                project_name = project_row[0]
                cur.execute("SELECT study_name FROM Studies WHERE study_id = %s", (study_id,))
                study_row = cur.fetchone()
                if not study_row:
                    raise Exception(f"Study id {study_id} not found in database")
                study_name = study_row[0]

                # 4. concatenate target directory
                target_dir = os.path.join(UPLOAD_FOLDER, secure_filename(project_name), secure_filename(study_name))
                os.makedirs(target_dir, exist_ok=True)

                # 5. concatenate file full path
                file_path = os.path.join(target_dir, file_name)

                # 6. save file
                file.save(file_path)
                file_size = str(os.path.getsize(file_path))

                # 7. write to Files table
                cur.execute(
                    "INSERT INTO Files (file_name, file_path, file_size, uploaded_by, description, study_id, species, genome_release, experiment_type, upload_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)",
                    (file_name, file_path, file_size, request.form.get('user_id'), request.form.get('description', ''), study_id, request.form.get('species', ''), request.form.get('genome_release', ''), request.form.get('experiment_type', ''))
                )
                conn.commit()
                success = f"File uploaded successfully to {file_path}"
            except Exception as e:
                error = f"Upload failed: {e}"

    conn.close()
    return render_template('upload.html',
                        projects=projects,
                        studies=studies,
                        users=users,
                        species_list=species_list,
                        genome_release_list=genome_release_list,
                        experiment_type_list=experiment_type_list,
                        error=error,
                        success=success)

@app.route('/test3/projects')
@login_required
def show_projects():
    conn = get_db_connection()
    cur = conn.cursor()
    # get all projects 
    cur.execute("SELECT project_id, project_name FROM Projects ORDER BY project_name")
    projects_raw = cur.fetchall()
    projects = []
    for p in projects_raw:
        project_id, project_name = p
        # get all studies in this project
        cur.execute("SELECT study_id, study_name, description FROM Studies WHERE project_id = %s ORDER BY study_name", (project_id,))
        studies_raw = cur.fetchall()
        studies = []
        for s in studies_raw:
            study_id, study_name, study_desc = s
            # get all files in this study
            cur.execute("SELECT file_name, file_path, description FROM Files WHERE study_id = %s", (study_id,))
            files = [{'file_name': f[0], 'file_path': f[1], 'description': f[2]} for f in cur.fetchall()]
            studies.append({'study_id': study_id, 'study_name': study_name, 'description': study_desc, 'files': files})
        projects.append({'project_name': project_name, 'studies': studies})

    # count the number of files in each study
    cur.execute("""
        SELECT s.study_name, COUNT(f.file_id)
        FROM Files f
        JOIN Studies s ON f.study_id = s.study_id
        GROUP BY s.study_name
        ORDER BY s.study_name
    """)
    files_per_study = cur.fetchall()

    # count the number of files in each genome_release
    cur.execute("""
        SELECT genome_release, COUNT(*) 
        FROM Files 
        WHERE genome_release IS NOT NULL AND genome_release != ''
        GROUP BY genome_release
        ORDER BY genome_release
    """)
    files_per_genome = cur.fetchall()

    # count the number of files in each species
    cur.execute("""
        SELECT species, COUNT(*) 
        FROM Files 
        WHERE species IS NOT NULL AND species != ''
        GROUP BY species
        ORDER BY species
    """)
    files_per_species = cur.fetchall()

    # convert to JS usable format
    study_data = [['Study', 'Count']] + list(files_per_study)
    genome_data = [['Genome Release', 'Count']] + list(files_per_genome)
    species_data = [['Species', 'Count']] + list(files_per_species)

    conn.close()
    return render_template(
        'studies.html',
        projects=projects,
        user_urole=session.get('urole', 'guest'),
        study_data=json.dumps(study_data),
        genome_data=json.dumps(genome_data),
        species_data=json.dumps(species_data)
    )



@app.route('/test3/help')
def help_page():
    return render_template('help.html')

@app.route('/test3/home')
@login_required
def home_page():
    print(f"home page, session: {session}")
    user_urole = session.get('urole', 'guest')
    conn = get_db_connection()
    if not conn:
        return render_template('home.html', 
            total_projects=0,
            total_files=0,
            total_users=0,
            total_analyses=0,
            user_urole=user_urole
        )
    
    try:
        cur = conn.cursor()
        
        # Get statistics data
        cur.execute("SELECT COUNT(*) FROM Projects")
        total_projects = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(*) FROM Files")
        total_files = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(*) FROM Users")
        total_users = cur.fetchone()[0]
        
        total_analyses = 0  # If there is no analyses table, default to 0
        
        return render_template('home.html',
            total_projects=total_projects,
            total_files=total_files,
            total_users=total_users,
            total_analyses=total_analyses,
            user_urole=user_urole
        )
        
    except Exception as e:
        print(f"Error loading statistics data: {e}")
        return render_template('home.html',
            total_projects=0,
            total_files=0,
            total_users=0,
            total_analyses=0,
            user_urole=user_urole
        )
    finally:
        if conn:
            conn.close()

@app.route('/test3/users')
def show_users():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Get all guest users
        cur.execute("""
            SELECT user_id, username, email, urole 
            FROM Users 
            WHERE urole = 'guest'
            ORDER BY username
        """)
        guest_results = cur.fetchall()
        
        # Get all users with their project associations
        query = """
            SELECT 
                u.user_id, 
                u.username, 
                u.email, 
                u.urole, 
                COALESCE(p.project_id, '') AS project_id, 
                COALESCE(p.project_name, 'No projects') AS project_name 
            FROM Users u
            LEFT JOIN users_in ui ON u.user_id = ui.user_id 
            LEFT JOIN Projects p ON ui.project_id = p.project_id 
            ORDER BY u.username, p.project_name
        """
        cur.execute(query)
        results = cur.fetchall()
        
        # Get count of all users
        cur.execute("SELECT COUNT(*) FROM Users")
        user_count = cur.fetchone()[0]
        
        cur.close()
        conn.close()

        return render_template(
            'users.html', 
            guest_results=guest_results, 
            results=results, 
            resultsAllUsers=f"All users in the system (Total: {user_count})"
        )

    except mariadb.Error as e:
        print(f"Error connecting to MariaDB: {e}")
        return render_template(
            'users.html', 
            guest_results=None, 
            results=None, 
            resultsAllUsers="Error loading user data"
        )
    
def convert_txt_to_bed(txt_file):
    try:
        # Read TXT file with tab separator  
        df = pd.read_csv(txt_file, sep='\t', header=None)
        
        # Ensure at least 3 columns (chromosome, start, end)
        if df.shape[1] < 3:
            return False, "TXT file must contain at least 3 columns: chromosome, start, end"
        
        # Rename the first three columns
        columns = ['chrom', 'start', 'end'] + [f'column_{i+4}' for i in range(df.shape[1]-3)]
        df.columns = columns
        
        # Generate output file name
        output_file = os.path.splitext(txt_file)[0] + '.bed'
        
        # Save as BED format
        df.to_csv(output_file, sep='\t', index=False, header=False)
        return True, output_file
    except Exception as e:
        return False, f"Conversion failed: {str(e)}"

def convert_csv_to_bed(csv_file):
    try:
        # Read CSV file
        df = pd.read_csv(csv_file)
        
        # Check required columns
        required_columns = ['chrom', 'start', 'end']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            return False, f"CSV file is missing required columns: {', '.join(missing_columns)}"
        
        # Select and rearrange columns
        columns = ['chrom', 'start', 'end'] + [col for col in df.columns if col not in required_columns]
        df = df[columns]
        
        # Generate output file name
        output_file = os.path.splitext(csv_file)[0] + '.bed'
        
        # Save as BED format
        df.to_csv(output_file, sep='\t', index=False, header=False)
        return True, output_file
    except Exception as e:
        return False, f"Conversion failed: {str(e)}"

@app.route('/test3/convert', methods=['GET', 'POST'])
def convert_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('convert.html', error="Please select a file")
        
        file = request.files['file']
        if file.filename == '':
            return render_template('convert.html', error="No file selected")
        
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            file_type = request.form.get('file_type')
            success = False
            message = ""
            
            if file_type == 'txt':
                success, message = convert_txt_to_bed(file_path)
            elif file_type == 'csv':
                success, message = convert_csv_to_bed(file_path)
            else:
                message = "Unsupported file type"
            
            if success:
                # If conversion is successful, message contains output file path
                return render_template('convert.html', 
                    success=f"File has been successfully converted to BED format",
                    output_file=os.path.basename(message))
            else:
                return render_template('convert.html', error=message)
    
    return render_template('convert.html')


@app.route('/test3/get_files', methods=['GET'])
@login_required
def get_files():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # get all projects
        cursor.execute("SELECT project_id, project_name FROM Projects ORDER BY project_name")
        projects = cursor.fetchall()

        # get all studies
        cursor.execute("SELECT study_id, study_name, project_id FROM Studies ORDER BY study_name")
        studies = cursor.fetchall()

        # get filters
        filters = {
            'project_id': request.args.get('project_id'),
            'study_id': request.args.get('study_id'),
            'species': request.args.get('species'),
            'genome': request.args.get('genome')
        }

        # 构建查询
        query = """
            SELECT f.file_name, f.file_path, f.file_size, f.upload_date, f.description,
                   s.study_id, s.study_name, p.project_id, p.project_name,
                   f.species, f.genome_release, f.experiment_type
            FROM Files f
            JOIN Studies s ON f.study_id = s.study_id
            JOIN Projects p ON s.project_id = p.project_id
            WHERE 1=1
        """
        params = []
        if filters['project_id']:
            query += " AND p.project_id = %s"
            params.append(filters['project_id'])
        if filters['study_id']:
            query += " AND s.study_id = %s"
            params.append(filters['study_id'])
        if filters['species']:
            query += " AND f.species = %s"
            params.append(filters['species'])
        if filters['genome']:
            query += " AND f.genome_release = %s"
            params.append(filters['genome'])

        cursor.execute(query, params)
        files = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify({
            'projects': projects,
            'studies': studies,
            'files': files
        })
    except mariadb.Error as e:
        return jsonify({'error': str(e)}), 500

@app.route('/test3/save_command', methods=['POST'])
@login_required  # add login verification
def save_command():
    try:
        data = request.json
        study_id = data.get('study_id')
        filenames = data.get('filenames')
        command = data.get('command')
        
        # save command to database
        print(f"Saved command for study {study_id}:")
        print(f"Files: {', '.join(filenames)}")
        print(f"Command: {command}")
        
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
@app.route('/test3/search')
@login_required
def search_page():
    return render_template('search.html')

@app.route('/test3/run_bedtools', methods=['POST'])
@login_required
def run_bedtools():
    data = request.json
    command = data.get('command')
    # full path of bedtools
    BEDTOOLS_PATH = '/usr/local/bedtools2/bin/bedtools'
    # replace bedtools in command with full path
    command = command.replace('bedtools', BEDTOOLS_PATH)
    # only allow bedtools commands, prevent injection
    if not command or not command.strip().startswith(BEDTOOLS_PATH):
        return jsonify({'error': 'Invalid command'}), 400
    try:
        # execute command, capture output
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=60)
        if result.returncode != 0:
            return jsonify({'error': result.stderr}), 500
        return jsonify({'output': result.stdout})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
