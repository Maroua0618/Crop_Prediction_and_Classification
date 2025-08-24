from flask import Blueprint, render_template, session, flash, redirect, url_for
from models import User

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/login_page')
def login_page():
    return render_template('login_page.html')

@main_bp.route('/signup_page')
def signup_page():
    return render_template('signup_page.html')

@main_bp.route('/profile')
def profile():
    if 'user_id' not in session:
        flash('Please login to view your profile')
        return redirect(url_for('main.login_page'))

    user = User.query.get(session['user_id'])
    return render_template('Profile.html', user=user)