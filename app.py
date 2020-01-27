from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "app.sqlite")

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Products(db.Model):
  __tablename__ = "products"
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(150), unique=True, nullable=False)
  shirt = db.Column(db.Boolean)
  hat = db.Column(db.Boolean)
  category = db.Column(db.String(100))
  price = db.Column(db.String(10))
  prodimg = db.Column(db.String(1000))
  size = db.Column(db.String(1000), nullable=True)
  quantity = db.Column(db.Integer)


  def __init__(self, title, shirt, hat, category, price, prodimg, size, quantity):
    self.title = title
    self.shirt = shirt
    self.hat = hat
    self.category = category
    self.price = price
    self.prodimg = prodimg
    self.size = size
    self.quantity = quantity

class ProductSchema(ma.Schema):
  class Meta:
    fields = ("id", "title", "shirt", "hat", "category", "price", "prodimg", "size", "quantity" )

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

# CRUD
# GET
@app.route("/products", methods=["GET"])
def get_products():
  all_products = Products.query.all()
  result = products_schema.dump(all_products)

  return jsonify(result)

# POST
@app.route("/product", methods=["POST"])
def add_product():
  title = request.json["title"]
  shirt = request.json["shirt"]
  hat = request.json["hat"]
  category = request.json["category"]
  price = request.json["price"]
  prodimg = request.json["prodimg"]
  size = request.json["size"]
  quantity = request.json["quantity"]

  new_product = Product(title, shirt, hat, category, price, prodimg, size, quantity)

  db.session.add(new_product)
  db.session.commit()

  product = Product.query.get(new_product.id)
  return product_schema.jsonify(product)


# PUT/PATCH by ID
# @app.route("/todo/<id>", methods=["PATCH"])
# def update_product(id):
#   product = Todo.query.get(id)

#   new_done = request.json["done"]

#   todo.done = new_done

#   db.session.commit()
#   return todo_schema.jsonify(todo)

# DELETE
@app.route("/product/<id>", methods=["DELETE"])
def delete_product(id):
  product = Product.query.get(id)
  db.session.delete(product)
  db.session.commit()

  return jsonify("Got rid of that ish!")

if __name__ == "__main__":
  app.debug = True
  app.run()