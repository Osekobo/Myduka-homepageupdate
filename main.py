from flask import Flask, render_template, request, redirect, url_for, flash, session
from database import get_products, get_sales, insert_products, insert_stock, get_stock, insert_sales, available_stock, sales_per_product, sales_per_day, profit_per_day, profit_per_product, check_user, insert_user, edited_product
from flask_bcrypt import Bcrypt
from functools import wraps
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin, current_user
import sqlalchemy


app = Flask(__name__)

app.secret_key = '123wtrdfdcxcf'

bcrypt = Bcrypt(app)


@app.route('/')
def home():
    return render_template("index.html")


def login_required(f):
    @wraps(f)
    def protected(*args, **kwargs):
        if 'email' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return protected


@app.route('/products')
def products():
    if 'email' not in session:
        return redirect(url_for('login'))
    products = get_products()
    return render_template("products.html", products=products)


@app.route('/sales')
@login_required
def sales():
    products = get_products()
    sales = get_sales()
    return render_template('sales.html', sales=sales, products=products)


@app.route('/stock')
@login_required
def stock():
    products = get_products()
    stock = get_stock()
    return render_template("stock.html", products=products, stock=stock)


@app.route('/add_products', methods=['GET', 'POST'])
def add_products():
    product_name = request.form['product_name']
    buying_price = request.form["buying"]
    selling_price = request.form["selling"]
    new_product = (product_name, buying_price, selling_price)
    insert_products(new_product)
    flash("Product added successfully!", "success")
    return redirect(url_for('products'))


@app.route('/add_stock', methods=['GET', 'POST'])
def add_stock():
    product_id = request.form['pid']
    stock_quantity = request.form['stock_quantity']
    new_stock = (product_id, stock_quantity)
    insert_stock(new_stock)
    flash("Stock added successfully!", "success")
    return redirect(url_for('stock'))


@app.route('/add_sales', methods=['GET', 'POST'])
def add_sales():
    product_id = request.form['id']
    sales_quantity = request.form['quantity']
    new_sales = (product_id, sales_quantity)
    stock_available = available_stock(product_id)
    if stock_available < float(sales_quantity):
        flash("Insufficient stock to complete sale", "danger")
    else:
        insert_sales(new_sales)
        flash("Sale made successfully!", "success")
    return redirect(url_for('sales'))  # sales is name of view function


# Dashboard
@app.route('/dashboard')
@login_required
def dashboard():
    sales_product = sales_per_product()
    profit_product = profit_per_product()
    sales_day = sales_per_day()
    profit_day = profit_per_day()

# product related dashboard data
    product_names = [i[0] for i in sales_product]
    sale_prod = [float(i[1])
                 for i in sales_product]  # float for js to understand
    prof_prod = [float(i[1]) for i in profit_product]


# date related dashboard data
    # list comprehension , what of diferent method
    date = [str(i[0]) for i in sales_day]
    sales_of_day = [float(i[1]) for i in sales_day]
    profit_of_day = [float(i[1]) for i in profit_day]

# day dashboard data
    date = [str(i[0]) for i in profit_day]
    prof_day = [float(i[1]) for i in profit_day]
    s_day = [float(i[1]) for i in sales_day]

    return render_template("dashboard.html", product_names=product_names, sale_prod=sale_prod, prof_prod=prof_prod, date=date, sales_of_day=sales_of_day, profit_of_day=profit_of_day, prof_day=prof_day, s_day=s_day)


# login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = check_user(email)
        if not user:
            flash("Incorrect user or password, Please try again!", "danger")
        else:
            if bcrypt.check_password_hash(user[-1], password):
                flash("Login successful", "success")
                session['email'] = email
                return redirect(url_for('products'))
            else:
                flash("Incorrect password, please try again", "danger")
    return render_template("login.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form['full_name']
        email = request.form['email']
        phone_number = request.form['phone_number']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(
            password).decode('utf-8')
        user = check_user(email)
        if not user:
            new_user = (full_name, email, phone_number, hashed_password)
            insert_user(new_user)
            flash("User registered successfully! Please login", "success")
            return redirect(url_for('login'))
        else:
            flash("User already registered, please login", "danger")
    return render_template("register.html")


@app.route('/logout')
@login_required
def logout():
    session.pop('email', None)
    flash("Logged out successfully", "info")
    return redirect(url_for('login'))


@app.route('/edited_prod', methods=['GET', 'POST'])
@login_required
def edit_pro():
    id = request.form['id']
    prod_name1 = request.form['name1']
    prod_name2 = request.form['name2']
    prod_name3 = request.form['name3']
    x = (prod_name1, prod_name2, prod_name3, id)
    edited_product(x)
    flash("Product edited")
    return redirect(url_for('products'))


app.run(debug=True)
