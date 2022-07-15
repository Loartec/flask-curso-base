#from my_app import app
from flask import Blueprint, render_template
from flask_restful import abort
from my_app.product.model.products import PRODUCTS

product = Blueprint('product', __name__)

@product.route('/')
@product.route('/home')
def index():
    return render_template('product/index.html', products=PRODUCTS)

@product.route('/product/<int:id>')
def show(id):
    product = PRODUCTS.get(id)

    if not product:
        abort(404)

    return render_template('product/show.html', product=product)

@product.route('/filter/<int:id>')
def filter(id):
    product = PRODUCTS.get(id)
    return render_template('product/filter.html', product=product)
