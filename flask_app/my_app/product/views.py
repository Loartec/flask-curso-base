#from my_app import app
from flask import Blueprint, redirect, render_template, request, url_for, flash, get_flashed_messages 
from flask_restful import abort
from sqlalchemy.sql.expression import not_,or_

from my_app import db
from my_app.product.model.products import PRODUCTS
from my_app.product.model.product import Product
from my_app.product.model.product import ProductForm


product = Blueprint('product', __name__)

@product.route('/product')
@product.route('/product/<int:page>')
def index(page=1):
    return render_template('product/index.html', products=Product.query.paginate(page,5))

@product.route('/product/<int:id>')
def show(id):
    product = Product.query.get_or_404(id)
    return render_template('product/show.html', product=product)

@product.route('/product-delete/<int:id>')
def delete(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    flash("Producto eliminado con éxito")

    return redirect(url_for('product.index'))

@product.route('/product-create', methods=['POST', 'GET'])
def create():
    form = ProductForm(meta={'csrf':False})
    if form.validate_on_submit():
        # Crear Producto
        p = Product(request.form['name'], request.form['price'])
        db.session.add(p)
        db.session.commit()
        flash("Producto creado con exito")    
        return redirect(url_for('product.create'))

    if form.errors:
        flash(form.errors, 'danger')

    return render_template('product/create.html', form=form)

@product.route('/product-update/<int:id>', methods=['GET','POST'])
def update(id):
    product = Product.query.get_or_404(id)
    form = ProductForm(meta={'csrf':False})

    if request.method == 'GET':
        form.name.data = product.name
        form.price.data = product.price

    if form.validate_on_submit():
        # Actualizar Producto
        product.name = form.name.data
        product.price = form.price.data
        
        db.session.add(product)
        db.session.commit()
        flash("Producto actualizado con exito")
        return redirect(url_for('product.update', id=product.id))

        if form.errors:
            flash(form.errors, 'danger')

    return render_template('product/update.html', product=product, form=form)
    
    
@product.route('/test')
def test():
    #p = Product.query.all()
    #print(p)

    # Crear Registros 
    """
    p = Product("P5", 60.8)
    db.session.add(p)
    db.session.commit()
    Product.add(p)
    """
    # Actualizar
    """
    p = Product.query.filter_by(name = "P1", id=1).first()
    p.name = "UP1"
    db.session.add(p)
    db.session.commit()
    """
    # Eliminar
    """
    p = Product.query.filter_by(id=1).first()
    db.session.delete(p)
    db.session.commit()
    """

    return "Flask"

@product.route('/filter/<int:id>')
def filter(id):
    product = PRODUCTS.get(id)
    return render_template('product/filter.html', product=product)
