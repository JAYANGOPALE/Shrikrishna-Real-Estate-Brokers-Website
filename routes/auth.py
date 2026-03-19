from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from models.user_model import User
from database.db import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login-choice')
def login_choice():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    return render_template('login_choice.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', 'danger')
            return redirect(url_for('auth.register'))

        new_user = User(name=name, email=email, phone=phone, is_admin=False)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        user = User.query.filter_by(email=email).first()

        if not user or user.is_admin or not user.check_password(password):
            flash('Invalid user credentials.', 'danger')
            return redirect(url_for('auth.login'))

        user.last_login_at = datetime.utcnow()
        db.session.commit()
        login_user(user, remember=remember)
        return redirect(url_for('main.index'))

    return render_template('user_login.html')

@auth_bp.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated:
        if current_user.is_admin:
            return redirect(url_for('admin.dashboard'))
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        user = User.query.filter_by(email=email).first()

        if not user or not user.is_admin or not user.check_password(password):
            flash('Invalid admin credentials.', 'danger')
            return redirect(url_for('auth.admin_login'))

        user.last_login_at = datetime.utcnow()
        db.session.commit()
        login_user(user, remember=remember)
        return redirect(url_for('admin.dashboard'))

    return render_template('admin_login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('main.index'))
