import mariadb

app = Flask(__name__)

# 数据库连接函数
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
@app.route('/')
def show():
    return render_template("test.html")

# 路由: 显示项目名称和研究名称
@app.route('/studies', methods=['GET'])
def studies():
    conn = get_db_connection()
    if not conn:
        return "Database connection failed", 500

    try:
        cur = conn.cursor()
        
        # 查询 Projects 表
        cur.execute("SELECT project_name FROM Projects")
        projects = cur.fetchall()  # 获取所有项目名称
        
        # 查询 Studies 表
        cur.execute("SELECT study_name FROM Studies")
        studies = cur.fetchall()  # 获取所有研究名称
        
    except mariadb.Error as e:
        print(f"Database error: {e}")
        return "Database operation failed", 500
    finally:
	conn.close()

    # 将数据传递给前端模板
    return render_template('test.html', projects=projects, studies=studies)

if __name__ == '__main__':
    app.run(debug=True)