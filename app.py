from flask import Flask, render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from config import Config
from models import db 

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = "secretkey"

# Initialize db with the app
db.init_app(app)

# Create tables (Flask 3 way)
with app.app_context():
    db.create_all()

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///store.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# ----------------------
# Database Model
# ----------------------

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Float)

# ----------------------
# Create Database + Add Shoes
# ----------------------

with app.app_context():
    db.create_all()
    if not Product.query.first():
        shoes = [
            Product(name="Nike Air Max", price=2500),
            Product(name="Adidas Ultraboost", price=2800),
            Product(name="Puma RS-X", price=2200),
            Product(name="Converse All Star", price=1800)
        ]
        db.session.add_all(shoes)
        db.session.commit()

# ----------------------
# Routes
# ----------------------

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/products")
def products():
    items = Product.query.all()
    return render_template("products.html", products=items)

@app.route("/add_to_cart/<int:product_id>")
def add_to_cart(product_id):
    if "cart" not in session:
        session["cart"] = []

    session["cart"].append(product_id)
    session.modified = True

    return redirect(url_for("cart"))

@app.route("/cart")
def cart():
    if "cart" not in session:
        session["cart"] = []

    cart_items = Product.query.filter(Product.id.in_(session["cart"])).all()
    total = sum(item.price for item in cart_items)

    return render_template("cart.html", items=cart_items, total=total)

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)

