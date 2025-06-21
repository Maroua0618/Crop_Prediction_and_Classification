from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import os
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a strong random key in production

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///farmeazy.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Define database models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<User {self.email}>'

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login_page')
def login_page():
    return render_template('login_page.html')

@app.route('/signup_page')
def signup_page():
    return render_template('signup_page.html')

@app.route('/profile')
def profile():
    # Check if user is logged in
    if 'user_id' not in session:
        flash('Please login to view your profile')
        return redirect(url_for('login_page'))
    
    # Get user from database
    user = User.query.get(session['user_id'])
    return render_template('Profile.html', user=user)

# API Routes for authentication
@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.form
    
    # Debug print to see what's being received
    print("Received signup data:", data)
    
    # Validate data
    if not data.get('fullName') or not data.get('signupEmail') or not data.get('signupPassword'):
        return jsonify({'success': False, 'message': 'Missing required fields'}), 400
    
    # Check if email already exists
    if User.query.filter_by(email=data.get('signupEmail')).first():
        return jsonify({'success': False, 'message': 'Email already registered'}), 400
    
    # Hash password
    hashed_password = bcrypt.generate_password_hash(data.get('signupPassword')).decode('utf-8')
    
    # Create new user
    new_user = User(
        full_name=data.get('fullName'),
        email=data.get('signupEmail'),
        password_hash=hashed_password
    )
    
    # Add user to database
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Account created successfully'}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.form
    
    # Debug print to see what's being received
    print("Received login data:", data)
    
    # Find user by email
    user = User.query.filter_by(email=data.get('email')).first()
    
    # Check if user exists and password is correct
    if user and bcrypt.check_password_hash(user.password_hash, data.get('password')):
        # Store user id in session
        session['user_id'] = user.id
        return jsonify({'success': True, 'message': 'Login successful'}), 200
    
    return jsonify({'success': False, 'message': 'Invalid email or password'}), 401

@app.route('/api/logout')
def logout():
    # Remove user from session
    session.pop('user_id', None)
    return redirect(url_for('index'))

# Prediction routes
@app.route('/prediction')
def prediction_page():
    return render_template('prediction.html')

@app.route('/api/predict', methods=['POST'])
def predict_crop():
    data = request.form
    
    # Debug print to see what's being received
    print("Received prediction data:", data)
    
    # Validate required fields
    required_fields = ['Nitrogen', 'Phosphorus', 'Potassium', 'Ph', 'Temperature', 'Humidity', 'Rainfall']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'success': False, 'message': f'Missing required field: {field}'}), 400
    
    # Here you would normally process the data with your ML model
    # For now, we'll redirect to the results page with the data
    # Store the prediction data in session for the results page
    session['prediction_data'] = {
        'nitrogen': float(data.get('Nitrogen')),
        'phosphorus': float(data.get('Phosphorus')),
        'potassium': float(data.get('Potassium')),
        'ph': float(data.get('Ph')),
        'temperature': float(data.get('Temperature')),
        'humidity': float(data.get('Humidity')),
        'rainfall': float(data.get('Rainfall'))
    }
    
    return jsonify({'success': True, 'redirect': '/prediction-results'}), 200

@app.route('/prediction-results')
def prediction_results():
    # Check if prediction data exists in session
    if 'prediction_data' not in session:
        flash('Please submit prediction data first')
        return redirect(url_for('prediction_page'))
    
    return render_template('predictionresult.html')

# Admin route to view database entries
@app.route('/admin/users')
def admin_users():
    # For development only - in production, add proper authentication
    users = User.query.all()
    user_list = []
    for user in users:
        user_list.append({
            'id': user.id,
            'full_name': user.full_name,
            'email': user.email,
            'created_at': user.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })
    return jsonify({'users': user_list})

# Create database tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)