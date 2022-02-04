from recetas_app import app
from recetas_app.controllers import sharedController, usersController, recipesController

if __name__ == '__main__':
    app.run( debug = True, port = 8091 )