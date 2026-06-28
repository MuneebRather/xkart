import json
import os
from functools import wraps

from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Needed for Flask sessions to work (cookie signing).
# For a real deployed app, set this from an environment variable instead.
app.secret_key = 'dev-secret-key-change-this'

USERS_FILE = 'users.json'


def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    return {}


def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)


def login_required(view_func):
    """Redirect to /login if there's no active session, remembering
    which page the user was trying to reach."""
    @wraps(view_func)
    def wrapped(*args, **kwargs):
        if 'user_email' not in session:
            return redirect(url_for('login', next=request.path))
        return view_func(*args, **kwargs)
    return wrapped


@app.route('/')
def root():
    # Public homepage — browsing doesn't require login, just like a real store.
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    next_url = request.args.get('next') or request.form.get('next')

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        users = load_users()
        user = users.get(email)

        if user and check_password_hash(user['password'], password):
            session['user_email'] = email
            session['user_name'] = user['name']
            # Only follow 'next' if it's a safe local path (avoids open redirects)
            if next_url and next_url.startswith('/'):
                return redirect(next_url)
            return redirect(url_for('dashboard'))

        error = 'Invalid email or password.'

    registered = request.args.get('registered')
    return render_template('login.html', error=error, registered=registered, next=next_url)


@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        name = request.form.get('fullname', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm = request.form.get('confirm', '')
        terms = request.form.get('terms')

        users = load_users()

        if not name or not email or not password:
            error = 'Please fill in all fields.'
        elif password != confirm:
            error = "Passwords don't match."
        elif not terms:
            error = 'You must accept the terms to continue.'
        elif email in users:
            error = 'An account with this email already exists.'
        else:
            users[email] = {
                'name': name,
                'password': generate_password_hash(password),
            }
            save_users(users)
            return redirect(url_for('login', registered=1))

    return render_template('register.html', error=error)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/products')
def products():
    return render_template('products.html')


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')



@app.route('/cart')
@login_required
def cart():
    return render_template('cart.html')


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')


@app.route('/settings')
@login_required
def settings():
    return render_template('settings.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)