from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_bcrypt import Bcrypt
from flask_app.models.user import User


bcrypt = Bcrypt(app)

@app.route('/')
def logReg():
    if 'user_id' not in session:
        return render_template('index.html')
    else:
        return redirect('/dashboard/')

@app.route('/register/', methods=['post'])
def register():
    isValid = User.validate(request.form)
    if not isValid:
        return redirect('/')
    else:
        newUser = {
            'firstName': request.form['firstName'],
            'lastName': request.form['lastName'],
            'email': request.form['email'],
            'password': bcrypt.generate_password_hash(request.form['password'])
        }
        id = User.save(newUser)
        if not id:
            flash('Something went wrong')
            return redirect('/')
        else:
            session['user_id'] = id
            flash("You are now logged in")
            return redirect('/dashboard/')

@app.route('/login/', methods=['POST'])
def login():
    data = {
        'email': request.form['email']
    }
    user = User.getEmail(data)
    if not user:
        flash('That email is not in our database please register')
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash('Wrong password')
        return redirect('/')
    else:
        session['user_id'] = user.id
        flash("You are now logged in")
        return redirect('/dashboard/')

@app.route('/logout/')
def logout():
    session.clear()
    return redirect('/')