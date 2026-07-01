
import os

from functools import wraps

from flask import Flask, render_template, request, redirect, url_for, session, jsonify
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

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(300))
    image = db.Column(db.String(100))

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(120), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    product = db.relationship('Product', backref='cart_items')

# ── Database seeding ────────────────────────────────────

def seed_products():
    if Product.query.count() == 0:
        products = [
            Product(name='Sony WH-1000XM5 Headphones', price=299.00,
                    category='Electronics',
                    description='Industry leading noise cancelling headphones.',
                    image='🎧'),
            Product(name='Nike Air Max 270', price=149.00,
                    category='Footwear',
                    description='Lightweight and comfortable running shoes.',
                    image='👟'),
            Product(name='Apple Watch SE 2nd Gen', price=249.00,
                    category='Electronics',
                    description='Powerful smartwatch with health tracking.',
                    image='⌚'),
            Product(name='Premium Leather Handbag', price=189.00,
                    category='Fashion',
                    description='Genuine leather handbag for everyday use.',
                    image='👜'),
            Product(name='Samsung 4K Monitor', price=399.00,
                    category='Electronics',
                    description='27 inch 4K UHD monitor for work and gaming.',
                    image='🖥️'),
            Product(name='Adidas Running Jacket', price=89.00,
                    category='Fashion',
                    description='Lightweight windproof running jacket.',
                    image='🧥'),
        ]
        db.session.add_all(products)
        db.session.commit()

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

# ── Product APIs ──────────────────────────────
@app.route('/api/products')
def api_products():
    products = Product.query.all()
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'price': p.price,
        'category': p.category,
        'description': p.description,
        'image': p.image
    } for p in products])

@app.route('/api/products/<int:product_id>')
def api_product(product_id):
    p = Product.query.get_or_404(product_id)
    return jsonify({
        'id': p.id,
        'name': p.name,
        'price': p.price,
        'category': p.category,
        'description': p.description,
        'image': p.image
    })

# ── Cart APIs ─────────────────────────────────
@app.route('/api/cart')
@login_required
def api_cart():
    email = session.get('user_email')
    items = CartItem.query.filter_by(user_email=email).all()
    return jsonify([{
        'id': item.id,
        'product_id': item.product_id,
        'name': item.product.name,
        'price': item.product.price,
        'image': item.product.image,
        'quantity': item.quantity,
        'total': item.product.price * item.quantity
    } for item in items])

@app.route('/api/cart/add', methods=['POST'])
@login_required
def api_cart_add():
    email = session.get('user_email')
    product_id = request.json.get('product_id')
    quantity = request.json.get('quantity', 1)

    existing = CartItem.query.filter_by(
        user_email=email,
        product_id=product_id
    ).first()

    if existing:
        existing.quantity += quantity
    else:
        item = CartItem(
            user_email=email,
            product_id=product_id,
            quantity=quantity
        )
        db.session.add(item)

    db.session.commit()
    return jsonify({'message': 'Added to cart successfully'})

@app.route('/api/cart/remove/<int:item_id>', methods=['DELETE'])
@login_required
def api_cart_remove(item_id):
    email = session.get('user_email')
    item = CartItem.query.filter_by(
        id=item_id,
        user_email=email
    ).first_or_404()
    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Removed from cart'})


# ── Create DB tables ──────────────────────────
with app.app_context():
    db.create_all()
    seed_products()

if __name__ == '__main__':
    app.run(debug=True)