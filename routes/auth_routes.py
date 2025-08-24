from flask import Blueprint, request, jsonify, session, redirect, url_for
from extensions import db, bcrypt
from models import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/api/signup', methods=['POST'])
def signup():
    data = request.form

    if not data.get('fullName') or not data.get('signupEmail') or not data.get('signupPassword'):
        return jsonify({'success': False, 'message': 'Missing required fields'}), 400

    if User.query.filter_by(email=data.get('signupEmail')).first():
        return jsonify({'success': False, 'message': 'Email already registered'}), 400

    hashed_password = bcrypt.generate_password_hash(data.get('signupPassword')).decode('utf-8')

    new_user = User(
        full_name=data.get('fullName'),
        email=data.get('signupEmail'),
        password_hash=hashed_password
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'success': True, 'message': 'Account created successfully'}), 201


   
@auth_bp.route('/api/login', methods=['POST'])
def login():
    data = request.form
    user = User.query.filter_by(email=data.get('email')).first()

    if user and bcrypt.check_password_hash(user.password_hash, data.get('password')):
        session['user_id'] = user.id
        return jsonify({'success': True, 'message': 'Login successful'}), 200

    return jsonify({'success': False, 'message': 'Invalid email or password'}), 401

@auth_bp.route('/api/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('main.index'))

