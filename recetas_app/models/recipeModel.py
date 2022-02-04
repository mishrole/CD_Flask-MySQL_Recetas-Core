from recetas_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
from recetas_app.models import userModel

TEXT_REGEX = re.compile(r'^.{3,}$')

class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.made_on = data['made_on']
        self.isUnder = data['isUnder']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = None

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes JOIN users ON recipes.author_id = users.id order by name asc;"
        results = connectToMySQL('recetas_schema').query_db(query)

        recipes = []

        if results:
            if len(results) > 0:
                for recipe in results:
                    current = cls(recipe)

                    print(recipe)

                    user_data = {
                        'id': recipe['users.id'],
                        'firstname': recipe['firstname'],
                        'lastname': recipe['lastname'],
                        'birthday': recipe['birthday'],
                        'gender': recipe['gender'],
                        'email': recipe['email'],
                        'password': recipe['password'],
                        'created_at': recipe['users.created_at'],
                        'updated_at': recipe['users.updated_at'],
                        'isBlocked': recipe['isBlocked']
                    }

                    current.user = userModel.User(user_data)
                    recipes.append(current)

        return recipes

    @classmethod
    def save(cls, data):
        query = "INSERT INTO recipes (name, description, instructions, made_on, isUnder, author_id, created_at, updated_at) VALUES (%(name)s, %(description)s, %(instructions)s, %(made_on)s, %(isUnder)s, %(authorId)s, NOW(), NOW());"
        return connectToMySQL('recetas_schema').query_db(query, data)

    @classmethod
    def update(cls, data):
        query = "UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, made_on = %(made_on)s, isUnder = %(isUnder)s, updated_at = NOW() WHERE recipes.id = %(recipeId)s;"
        return connectToMySQL('recetas_schema').query_db(query, data)

    @classmethod
    def findRecipeByIdWithAuthor(cls, data):
        query = "SELECT * FROM recipes JOIN users ON recipes.author_id = users.id WHERE recipes.id = %(recipeId)s;"
        results = connectToMySQL('recetas_schema').query_db(query, data)

        recipe = None

        if results:
            if len(results) > 0:
                recipe = cls(results[0])

                print(results[0])

                user_data = {
                    'id': results[0]['users.id'],
                    'firstname': results[0]['firstname'],
                    'lastname': results[0]['lastname'],
                    'birthday': results[0]['birthday'],
                    'gender': results[0]['gender'],
                    'email': results[0]['email'],
                    'password': results[0]['password'],
                    'created_at': results[0]['users.created_at'],
                    'updated_at': results[0]['users.updated_at'],
                    'isBlocked': results[0]['isBlocked']
                }

                recipe.user = userModel.User(user_data)
        
        return recipe

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM recipes WHERE recipes.id = %(recipeId)s;"
        return connectToMySQL('recetas_schema').query_db(query, data)

    @staticmethod
    def validateRecipe(data):
        is_valid = True

        name = data['name']
        description = data['description']
        instructions = data['instructions']
        made_on = data['made_on']
        isUnder = data['isUnder']

        if not TEXT_REGEX.match(name):
            flash('Name must be at least 3 characters long', 'form_cu_error')
            is_valid = False

        if len(description) < 3:
            flash('Description must be at least 3 characters long', 'form_cu_error')
            is_valid = False

        if len(instructions) < 3:
            flash('Description must be at least 3 characters long', 'form_cu_error')
            is_valid = False
        
        if len(made_on) == 0:
            flash('Select a date for made on', 'form_cu_error')
            is_valid = False

        if len(isUnder) == 0:
            flash('Select an option if is under 30 minutes or not', 'form_cu_error')
            is_valid = False

        return is_valid