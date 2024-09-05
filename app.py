from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure random key

# Sample product data
products = [
    {"id": 1, "name": "Product 1", "price": 100},
    {"id": 2, "name": "Product 2", "price": 200},
    {"id": 3, "name": "Product 3", "price": 300},
]

# Initialize an empty cart
cart = []

# Mock user data
users = {"user": "password"}  # Replace with a more secure method in production

@app.route('/')
def index():
    return render_template('index.html', products=products)

@app.route('/product/<int:product_id>')
def product(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if product is None:
        return "Product not found", 404
    return render_template('product.html', product=product)

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if product is not None:
        cart.append(product)
    return redirect(url_for('index'))

@app.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    global cart
    cart = [item for item in cart if item['id'] != product_id]
    return redirect(url_for('view_cart'))

@app.route('/cart')
def view_cart():
    return render_template('cart.html', cart=cart)

@app.route('/checkout')
def checkout():
    return render_template('checkout.html', cart=cart)

@app.route('/description')
def description():
    return render_template('description.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if users.get(username) == password:
            session['username'] = username
            return redirect(url_for('index'))
        return "Invalid credentials", 403
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
