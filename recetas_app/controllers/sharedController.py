from flask import Flask, redirect, render_template, session
from recetas_app import app

@app.errorhandler(404)
def page_not_found(error):
    app.logger.error(error)
    return render_template('404.html'), 404


@app.route('/', methods=['GET'])
def index():
    isLogged = False

    if 'userId' in session:
        isLogged = True
        return redirect('/dashboard')

    return render_template("index.html", isLogged = isLogged)


@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect('/')


@app.route('/blocked', methods=['GET'])
def blocked():
    return render_template('blocked.html')
