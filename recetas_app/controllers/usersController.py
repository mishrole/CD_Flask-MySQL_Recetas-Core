from flask import Flask, render_template, request, redirect, session, flash
from recetas_app import app
from recetas_app.models import userModel
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/register', methods=['POST'])
def register():
    if not userModel.User.validateRegister(request.form):
        return redirect('/')
    
    encryptedPassword = bcrypt.generate_password_hash(request.form['password'])

    gender = request.form['gender']
    
    if gender == 'Self describe':
        gender = request.form['other']

    data = {
        'firstname': request.form['firstname'],
        'lastname': request.form['lastname'],
        'email': request.form['email'],
        'password': encryptedPassword,
        'gender': gender,
        'birthday': request.form['birthday']
    }

    result = userModel.User.save(data)

    if type (result) is int and result > 0:
        session['userId'] = result
        return redirect('/dashboard')
    else:
        return redirect('/')


@app.route('/login', methods=['POST'])
def login():
    data = {
        'email': request.form['email'],
        'password': request.form['password']
    }

    if not userModel.User.validateLogin(data):
        return redirect('/')

    user = userModel.User.findUserByEmail(data)

    if user != None:
        if user.blockUser == True:
            return redirect('/blocked')

        if not bcrypt.check_password_hash(user.password, request.form['password']):
            flash('Invalid Email / Password', 'login_error')
            return redirect('/')
    
        session['userId'] = user.id
        return redirect('/dashboard')

