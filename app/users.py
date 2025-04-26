from flask import render_template, flash, redirect, url_for, request, session
from app import app
import mariadb
from app.config import get_db_connection
from functools import wraps

@app.route('/users')
def show_users():
    # Check if user is logged in
    if 'user_id' not in session:
        flash('Authentication required', 'error')
        return redirect(url_for('login'))
    
    # Check if user is admin
    if session.get('urole') != 'admin':
        flash('Access denied. Admin rights required', 'error')
        return redirect(url_for('home'))
    
    try:
        conn = get_db_connection()
        if conn is None:
            flash('Database connection error', 'error')
            return render_template('users.html', users=None)
            
        cur = conn.cursor(dictionary=True)
        
        cur.execute("SELECT user_id, username, email, urole FROM Users")
        users = cur.fetchall()
        
        cur.close()
        conn.close()
        
        return render_template('users.html', users=users)
        
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB: {e}")
        flash(f'Database error: {str(e)}', 'error')
        return render_template('users.html', users=None)

@app.route('/users/create', methods=['GET', 'POST'])
def create_user():
    # Check if user is logged in
    if 'user_id' not in session:
        flash('Authentication required', 'error')
        return redirect(url_for('login'))
    
    # Check if user is admin
    if session.get('urole') != 'admin':
        flash('Access denied. Admin rights required', 'error')
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('urole')
        
        if not all([username, email, password, role]):
            flash('All fields are required', 'error')
            return redirect(url_for('create_user'))
        
        try:
            conn = get_db_connection()
            if conn is None:
                flash('Database connection error', 'error')
                return redirect(url_for('create_user'))
                
            cur = conn.cursor(dictionary=True)
            
            # Check if user with this username already exists
            cur.execute("SELECT user_id FROM Users WHERE username = %s", (username,))
            if cur.fetchone():
                flash('User with this username already exists', 'error')
                return redirect(url_for('create_user'))
            
            # Check if user with this email already exists
            cur.execute("SELECT user_id FROM Users WHERE email = %s", (email,))
            if cur.fetchone():
                flash('User with this email already exists', 'error')
                return redirect(url_for('create_user'))
            
            # Add new user
            cur.execute(
                "INSERT INTO Users (username, email, password, urole) VALUES (%s, %s, %s, %s)",
                (username, email, password, role)
            )
            conn.commit()
            
            cur.close()
            conn.close()
            
            flash('User created successfully', 'success')
            return redirect(url_for('show_users'))
            
        except mariadb.Error as e:
            print(f"Error creating user: {e}")
            flash(f'Error creating user: {str(e)}', 'error')
            return redirect(url_for('create_user'))
    
    # GET request - display creation form
    return render_template('create_user.html')

@app.route('/users/edit/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    # Check if user is logged in
    if 'user_id' not in session:
        flash('Authentication required', 'error')
        return redirect(url_for('login'))
    
    # Check if user is admin
    if session.get('urole') != 'admin':
        flash('Access denied. Admin rights required', 'error')
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        role = request.form.get('urole')
        
        if not all([username, email, role]):
            flash('All fields are required', 'error')
            return redirect(url_for('show_users'))
        
        try:
            conn = get_db_connection()
            if conn is None:
                flash('Database connection error', 'error')
                return redirect(url_for('show_users'))
                
            cur = conn.cursor(dictionary=True)
            
            # Check if user with this ID exists
            cur.execute("SELECT user_id FROM Users WHERE user_id = %s", (user_id,))
            if not cur.fetchone():
                flash('User not found', 'error')
                return redirect(url_for('show_users'))
            
            # Update user data
            cur.execute(
                "UPDATE Users SET username = %s, email = %s, urole = %s WHERE user_id = %s",
                (username, email, role, user_id)
            )
            conn.commit()
            
            cur.close()
            conn.close()
            
            flash('User updated successfully', 'success')
            return redirect(url_for('show_users'))
            
        except mariadb.Error as e:
            print(f"Error updating user: {e}")
            flash(f'Error updating user: {str(e)}', 'error')
            return redirect(url_for('show_users'))
    
    # GET request - display edit form
    try:
        conn = get_db_connection()
        if conn is None:
            flash('Database connection error', 'error')
            return redirect(url_for('show_users'))
            
        cur = conn.cursor(dictionary=True)
        
        cur.execute("SELECT user_id, username, email, urole FROM Users WHERE user_id = %s", (user_id,))
        user = cur.fetchone()
        
        cur.close()
        conn.close()
        
        if not user:
            flash('User not found', 'error')
            return redirect(url_for('show_users'))
        
        return render_template('edit_user.html', user=user)
        
    except mariadb.Error as e:
        print(f"Error fetching user: {e}")
        flash(f'Error retrieving user data: {str(e)}', 'error')
        return redirect(url_for('show_users'))

@app.route('/users/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    # Check if user is logged in
    if 'user_id' not in session:
        flash('Authentication required', 'error')
        return redirect(url_for('login'))
    
    # Check if user is admin
    if session.get('urole') != 'admin':
        flash('Access denied. Admin rights required', 'error')
        return redirect(url_for('home'))
    
    # Prevent deleting your own account
    if user_id == session.get('user_id'):
        flash('You cannot delete your own account', 'error')
        return redirect(url_for('show_users'))
    
    try:
        conn = get_db_connection()
        if conn is None:
            flash('Database connection error', 'error')
            return redirect(url_for('show_users'))
            
        cur = conn.cursor()
        
        # Check if user with this ID exists
        cur.execute("SELECT user_id FROM Users WHERE user_id = %s", (user_id,))
        if not cur.fetchone():
            flash('User not found', 'error')
            return redirect(url_for('show_users'))
        
        # Delete user
        cur.execute("DELETE FROM Users WHERE user_id = %s", (user_id,))
        conn.commit()
        
        cur.close()
        conn.close()
        
        flash('User deleted successfully', 'success')
        return redirect(url_for('show_users'))
        
    except mariadb.Error as e:
        print(f"Error deleting user: {e}")
        flash(f'Error deleting user: {str(e)}', 'error')
        return redirect(url_for('show_users'))
