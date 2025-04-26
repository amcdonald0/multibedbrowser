from flask import render_template, flash, redirect, url_for, request, session
from app import app
import mariadb
from app.config import get_db_connection
from functools import wraps

# Decorator для проверки прав администратора
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Требуется авторизация', 'error')
            return redirect(url_for('login'))
        if session.get('urole') != 'admin':
            flash('Доступ запрещен. Требуются права администратора', 'error')
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/users')
@admin_required
def show_users():
    try:
        conn = get_db_connection()
        if conn is None:
            flash('Ошибка подключения к базе данных', 'error')
            return render_template('users.html', users=None)
            
        cur = conn.cursor(dictionary=True)
        
        cur.execute("SELECT user_id, username, email, urole FROM Users")
        users = cur.fetchall()
        
        cur.close()
        conn.close()
        
        return render_template('users.html', users=users)
        
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB: {e}")
        flash(f'Ошибка базы данных: {str(e)}', 'error')
        return render_template('users.html', users=None)

@app.route('/users/create', methods=['GET', 'POST'])
@admin_required
def create_user():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('urole')
        
        if not all([username, email, password, role]):
            flash('Все поля обязательны для заполнения', 'error')
            return redirect(url_for('create_user'))
        
        try:
            conn = get_db_connection()
            if conn is None:
                flash('Ошибка подключения к базе данных', 'error')
                return redirect(url_for('create_user'))
                
            cur = conn.cursor(dictionary=True)
            
            # Проверка, существует ли пользователь с таким именем
            cur.execute("SELECT user_id FROM Users WHERE username = %s", (username,))
            if cur.fetchone():
                flash('Пользователь с таким именем уже существует', 'error')
                return redirect(url_for('create_user'))
            
            # Проверка, существует ли пользователь с таким email
            cur.execute("SELECT user_id FROM Users WHERE email = %s", (email,))
            if cur.fetchone():
                flash('Пользователь с таким email уже существует', 'error')
                return redirect(url_for('create_user'))
            
            # Добавление нового пользователя
            cur.execute(
                "INSERT INTO Users (username, email, password, urole) VALUES (%s, %s, %s, %s)",
                (username, email, password, role)
            )
            conn.commit()
            
            cur.close()
            conn.close()
            
            flash('Пользователь успешно создан', 'success')
            return redirect(url_for('show_users'))
            
        except mariadb.Error as e:
            print(f"Error creating user: {e}")
            flash(f'Ошибка создания пользователя: {str(e)}', 'error')
            return redirect(url_for('create_user'))
    
    # GET запрос - отображение формы создания
    return render_template('create_user.html')

@app.route('/users/edit/<int:user_id>', methods=['GET', 'POST'])
@admin_required
def edit_user(user_id):
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        role = request.form.get('urole')
        
        if not all([username, email, role]):
            flash('Все поля обязательны для заполнения', 'error')
            return redirect(url_for('show_users'))
        
        try:
            conn = get_db_connection()
            if conn is None:
                flash('Ошибка подключения к базе данных', 'error')
                return redirect(url_for('show_users'))
                
            cur = conn.cursor(dictionary=True)
            
            # Проверка, существует ли пользователь с таким ID
            cur.execute("SELECT user_id FROM Users WHERE user_id = %s", (user_id,))
            if not cur.fetchone():
                flash('Пользователь не найден', 'error')
                return redirect(url_for('show_users'))
            
            # Обновление данных пользователя
            cur.execute(
                "UPDATE Users SET username = %s, email = %s, urole = %s WHERE user_id = %s",
                (username, email, role, user_id)
            )
            conn.commit()
            
            cur.close()
            conn.close()
            
            flash('Пользователь успешно обновлен', 'success')
            return redirect(url_for('show_users'))
            
        except mariadb.Error as e:
            print(f"Error updating user: {e}")
            flash(f'Ошибка обновления пользователя: {str(e)}', 'error')
            return redirect(url_for('show_users'))
    
    # GET запрос - отображение формы редактирования
    try:
        conn = get_db_connection()
        if conn is None:
            flash('Ошибка подключения к базе данных', 'error')
            return redirect(url_for('show_users'))
            
        cur = conn.cursor(dictionary=True)
        
        cur.execute("SELECT user_id, username, email, urole FROM Users WHERE user_id = %s", (user_id,))
        user = cur.fetchone()
        
        cur.close()
        conn.close()
        
        if not user:
            flash('Пользователь не найден', 'error')
            return redirect(url_for('show_users'))
        
        return render_template('edit_user.html', user=user)
        
    except mariadb.Error as e:
        print(f"Error fetching user: {e}")
        flash(f'Ошибка получения данных пользователя: {str(e)}', 'error')
        return redirect(url_for('show_users'))

@app.route('/users/delete/<int:user_id>', methods=['POST'])
@admin_required
def delete_user(user_id):
    # Запрещаем удаление своего аккаунта
    if user_id == session.get('user_id'):
        flash('Вы не можете удалить свой аккаунт', 'error')
        return redirect(url_for('show_users'))
    
    try:
        conn = get_db_connection()
        if conn is None:
            flash('Ошибка подключения к базе данных', 'error')
            return redirect(url_for('show_users'))
            
        cur = conn.cursor()
        
        # Проверка, существует ли пользователь с таким ID
        cur.execute("SELECT user_id FROM Users WHERE user_id = %s", (user_id,))
        if not cur.fetchone():
            flash('Пользователь не найден', 'error')
            return redirect(url_for('show_users'))
        
        # Удаление пользователя
        cur.execute("DELETE FROM Users WHERE user_id = %s", (user_id,))
        conn.commit()
        
        cur.close()
        conn.close()
        
        flash('Пользователь успешно удален', 'success')
        return redirect(url_for('show_users'))
        
    except mariadb.Error as e:
        print(f"Error deleting user: {e}")
        flash(f'Ошибка удаления пользователя: {str(e)}', 'error')
        return redirect(url_for('show_users'))
