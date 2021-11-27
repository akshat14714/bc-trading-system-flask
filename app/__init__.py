from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from flask_login import LoginManager
# from flask_migrate import Migrate

# from config import app_config, SQLALCHEMY_DATABASE_URI, SECRET_KEY

app = Flask(__name__)

app.config.from_object('config')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from app.home.controllers import home
from app.user.controller import mod_user

app.register_blueprint(home)
app.register_blueprint(mod_user)

db.create_all()

# def create_app():
#     app = Flask(__name__, instance_relative_config=True)
#     app.config.from_object('config')
#     db.app = app
#     db.init_app(app)
#
#     from app.user.controller import mod_user
#     app.register_blueprint(mod_user)
#
#     # @app.route('/')
#     # def index():
#     #     return 'Under Construction'
#
#     db.create_all()
#
#     return app
