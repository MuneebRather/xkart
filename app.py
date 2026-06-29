
import os

from functools import wraps

from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'xkart-secret-key-2026'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///xkart.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ── Models ────────────────────────────────────
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# ── Auth decorator ────────────────────────────
def login_required(view_func):
   
    @wraps(view_func)
    def wrapped(*args, **kwargs):
        if 'user_email' not in session:
            return redirect(url_for('login', next=request.path))
        return view_func(*args, **kwargs)
    return wrapped

# ── Routes ────────────────────────────────────
@app.route('/')

def root():
   
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
        try:
            user = User.query.filter_by(email=email).first()
        except Exception:
            user = None

        if user and check_password_hash(user.password, password):
            session['user_email'] = email
            session['user_name'] = user.name
            if next_url and next_url.startswith('/'):
                return redirect(next_url)
            return redirect(url_for('dashboard'))

        error = 'Invalid email or password.'

    registered = request.args.get('registered')
    return render_template('login.html', error=error,
                           registered=registered, next=next_url)

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        name = request.form.get('fullname', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm = request.form.get('confirm', '')
        terms = request.form.get('terms')



        if not name or not email or not password:
            error = 'Please fill in all fields.'
        elif password != confirm:
            error = "Passwords don't match."
        elif not terms:
            error = 'You must accept the terms to continue.'
        
        else:
            existing = User.query.filter_by(email=email).first()
            if existing:
                error = 'An account with this email already exists.'
            else:
                new_user = User(
                    name=name,
                    email=email,
                    password=generate_password_hash(password)
                )
                db.session.add(new_user)
                db.session.commit()
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

# ── Create DB tables ──────────────────────────
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)