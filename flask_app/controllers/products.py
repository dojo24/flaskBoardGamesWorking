from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_app.models.user import User
from flask_app.models.product import Product
from flask_app.models.orderd import Ordered


@app.route('/dashboard/')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    else:
        data = {
            'id': session['user_id']
        }
        theUser = User.getOne(data)
        # theItems = Product.getAll()
        theUsers = User.getAll()
        theItems = Product.allItemsNumberOrdered()
        return render_template('dashboard.html', user=theUser, items=theItems, users=theUsers)


@app.route('/addProduct/')
def addProduct():
    if 'user_id' not in session:
        return redirect('/')
    else:
        data = {
            'id': session['user_id']
        }
        theUser = User.getOne(data)
        return render_template('addProduct.html', user=theUser)

@app.route('/createProduct/', methods=['post'])
def createProduct():
    data = {
        'item': request.form['item'],
        'info': request.form['info'],
        'price': request.form['price'],
        'user_id': session['user_id'],
    }
    Product.save(data)
    return redirect('/dashboard/')

@app.route('/product/<int:product_id>/view/')
def viewProduct(product_id):
    if 'user_id' not in session:
        return redirect('/')
    else:
        data = {
            'id': session['user_id']
        }
        itemData = {
            'id': product_id
        }
        theUser = User.getOne(data)
        # theItem = Product.getOne(itemData) # Before adding in join statement
        theItem = Product.creator(itemData) # After adding in join
        theOrders = Product.allWhoOrdered(itemData)
        # print('theOrders', theOrders)
        return render_template('viewProduct.html', user=theUser, item=theItem, orders=theOrders)

@app.route('/product/<int:product_id>/order/', methods=['post'])
def order(product_id):
    data = {
        'product_id': product_id,
        'user_id': session['user_id']
    }
    Ordered.save(data)
    return redirect(f'/product/{product_id}/view/')

@app.route('/product/<int:product_id>/edit/')
def editProduct(product_id):
    if 'user_id' not in session:
        return redirect('/')
    else:
        data = {
            'id': session['user_id']
        }
        theUser = User.getOne(data)
        itemData = {
            'id': product_id
        }
        theItem = Product.getOne(itemData)
        return render_template('editProduct.html', user=theUser, item=theItem)

@app.route('/product/<int:product_id>/update/', methods=['post'])
def updateProduct(product_id):
    data = {
        'id': product_id,
        'item': request.form['item'],
        'info': request.form['info'],
        'price': request.form['price']
    }
    Product.update(data)
    return redirect(f'/product/{product_id}/view/')

@app.route('/product/<int:product_id>/delete/')
def deleteProduct(product_id):
    data = {
        'id': product_id
    }
    Product.delete(data)
    return redirect('/dashboard/')