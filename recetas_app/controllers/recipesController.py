from flask import Flask, render_template, request, redirect, session, flash
from recetas_app import app
from recetas_app.models import reportModel, userModel, recipeModel

# Render templates

@app.route('/dashboard', methods=['GET'])
def dashboard():
    userId = None

    if 'userId' in session:
        userId = session['userId']
        isLogged = True

        currentUser = userModel.User.findUserById({'userId': userId})

        # Si hay userId pero no encuentra un usuario, hace logout
        if currentUser == None:
            return redirect('/logout')

        recipes = recipeModel.Recipe.get_all()

        return render_template(
            'dashboard.html',
            currentUser = currentUser,
            isLogged = isLogged,
            recipes = recipes
        )
    else:
        return redirect('/')


@app.route('/recipes/details/<int:recipeId>', methods=['GET'])
def details_recipe_view(recipeId):
    userId = None

    if 'userId' in session:
        userId = session['userId']
        isLogged = True

    currentUser = userModel.User.findUserById({'userId': userId})

    if currentUser == None:
        return redirect('/logout')

    recipe = recipeModel.Recipe.findRecipeByIdWithAuthor({'recipeId': recipeId})

    if recipe == None:
        flash (f'Recipe with id {recipeId} not found', 'global_error')
        return redirect('/')

    return render_template('details_view.html', isLogged = isLogged, currentUser = currentUser, recipe = recipe)


@app.route('/recipes/new', methods=['GET'])
def create_recipe_view():
    userId = None

    if 'userId' in session:
        userId = session['userId']
        isLogged = True

    currentUser = userModel.User.findUserById({'userId': userId})

    if currentUser == None:
        return redirect('/logout')

    return render_template('create_form.html', isLogged = isLogged, currentUser = currentUser, userId = userId)


@app.route('/recipes/edit/<int:recipeId>', methods=['GET'])
def edit_recipe_view(recipeId):
    userId = None

    if 'userId' in session:
        userId = session['userId']
        isLogged = True

    currentUser = userModel.User.findUserById({'userId': userId})

    if currentUser == None:
        return redirect('/logout')

    recipe = recipeModel.Recipe.findRecipeByIdWithAuthor({'recipeId': recipeId})

    if recipe == None:
        flash (f'Recipe with id {recipeId} not found', 'global_error')
        return redirect('/')

    # Intenta ingresar a la vista de una receta que no le pertenece
    if recipe.user.id != currentUser.id:
        report = {
            'userId': currentUser.id,
            'userIp': request.remote_addr
        }

        reportModel.Report.save(report)
        reports = reportModel.Report.get_all_by_userId(report)

        if reports != None:
            if len(reports) == 1:
                return redirect('/danger')
            elif len(reports) > 1:
                userModel.User.blockUser(report)
                session.pop('userId')
                return redirect('/blocked')

        return redirect('/')

    return render_template('edit_form.html', isLogged = isLogged, currentUser = currentUser, recipe = recipe)


@app.route('/danger', methods=['GET'])
def danger():
    if 'userId' in session:
        userId = session['userId']

        data = {
            'userId': userId
        }

        report = reportModel.Report.findLastReportByUserId(data)

    return render_template('danger.html', report = report)


# Create, Update, Delete (Post)

@app.route('/recipes/form/new/<int:authorId>', methods=['POST'])
def create_recipe_form(authorId):

    if not recipeModel.Recipe.validateRecipe(request.form):
        return redirect('/recipes/new')

    if userModel.User.findUserById({'userId': authorId}) == None:
        return redirect('/logout')

    data = {
        'name': request.form['name'],
        'description': request.form['description'],
        'instructions': request.form['instructions'],
        'made_on': request.form['made_on'],
        'isUnder': request.form['isUnder'],
        'authorId': authorId
    }

    result = recipeModel.Recipe.save(data)

    if type (result) is int and result > 0:
        return redirect('/')
    else:
        flash('An error occurred. Please try again', 'form_cu_error')
        return redirect('/recipes/new')


@app.route('/recipes/form/edit/<int:recipeId>', methods=['POST'])
def update_recipe_form(recipeId):

    if not recipeModel.Recipe.validateRecipe(request.form):
        return redirect(f'/recipes/edit/{recipeId}')

    data = {
        'recipeId': recipeId,
        'name': request.form['name'],
        'description': request.form['description'],
        'instructions': request.form['instructions'],
        'made_on': request.form['made_on'],
        'isUnder': request.form['isUnder']
    }

    recipeModel.Recipe.update(data)
    return redirect('/')


@app.route('/recipes/form/delete/<int:recipeId>', methods=['POST'])
def delete_recipe_form(recipeId):

    if 'userId' in session:
        userId = session['userId']

    currentUser = userModel.User.findUserById({'userId': userId})

    if currentUser == None:
        return redirect('/logout')

    recipe = recipeModel.Recipe.findRecipeByIdWithAuthor({'recipeId': recipeId})

    if recipe == None:
        flash (f'Recipe with id {recipeId} not found', 'global_error')
        return redirect('/')

    if recipe.user.id != currentUser.id:

        report = {
            'userId': currentUser.id,
            'userIp': request.remote_addr
        }

        reportModel.Report.save(report)
        reports = reportModel.Report.get_all_by_userId(report)

        if reports != None:
            if len(reports) == 1:
                return redirect('/danger')
            elif len(reports) > 1:
                userModel.User.blockUser(report)
                session.pop('userId')
                return redirect('/blocked')
        
        return redirect('/')
    else:
        recipeModel.Recipe.delete({'recipeId': recipeId})
        flash (f'Recipe with id {recipeId} was deleted', 'global_success')
        return redirect('/')
    
