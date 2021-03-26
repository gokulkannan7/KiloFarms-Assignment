from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow 
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Product(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100))
  category = db.Column(db.String(200))
  price = db.Column(db.Float)

  def __init__(self, name, category, price):
    self.name = name
    self.category = category
    self.price = price

class ProductSchema(ma.Schema):
  class Meta:
    fields = ('id', 'name', 'category', 'price')

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)


@app.route('/createSKU', methods=['POST'])
def add_product():
  name = request.json['name']
  category = request.json['category']
  price = request.json['price']

  new_product = Product(name, category, price)

  db.session.add(new_product)
  db.session.commit()

  return product_schema.jsonify(new_product)

@app.route('/get', methods=['GET'])
def get_products():
  all_products = Product.query.all()
  result = products_schema.dump(all_products)
  return jsonify(result.data)


@app.route('/get/<id>', methods=['GET'])
def get_product(id):
  product = Product.query.get(id)
  return product_schema.jsonify(product)


@app.route('/update/<id>', methods=['PUT'])
def update_product(id):
  product = Product.query.get(id)

  name = request.json['name']
  category = request.json['category']
  price = request.json['price']

  product.name = name
  product.category = category
  product.price = price

  db.session.commit()

  return product_schema.jsonify(product)

@app.route('/product/<id>', methods=['DELETE'])
def delete_product(id):
  product = Product.query.get(id)
  db.session.delete(product)
  db.session.commit()

  return product_schema.jsonify(product)

if __name__ == '__main__':
  app.run(debug=True)