#this file tells python that this is a package and initializes and ties together all
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flaskblogmy.config import Config

#extensions ouside of function - so that one extention objects for more apps
db = SQLAlchemy() # database set up
bcrypt = Bcrypt()
login_manager = LoginManager() # we add some functionality to our database models and it will handle all of the sessions in the background for us.
login_manager.login_view = 'users.login' # for @login_required in routes /account
login_manager.login_mjessage_category = 'info' # nicer notification
mail = Mail()


#no blueprints -> from flaskblogmy import routes (here to avoid circular imports, probably enough to import them and they work?)


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from flaskblogmy.users.routes import users
    from flaskblogmy.posts.routes import posts
    from flaskblogmy.main.routes import main
    from flaskblogmy.errors.handlers import errors # necessary to register blueprint instance in app here.
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app

