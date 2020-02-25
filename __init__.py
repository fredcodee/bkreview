from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()

def create_app():
  app = Flask(__name__)

  app.config['SECRET_KEY'] = 'ASpire2begreat'
  app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://cajflrevfbywfx:3259245e928346a9eb88e48cb28d93c7e369b044ce6adde32ee7cda98af2019c@ec2-184-72-235-80.compute-1.amazonaws.com:5432/dbrbakv104v2pv"

  db.init_app(app)

  login_manager = LoginManager()
  login_manager.login_view = 'auth.login'
  login_manager.init_app(app)


  from .models import User
  @login_manager.user_loader
  def load_user(user_id):
    return(User.query.get(int(user_id)))


  # blueprint for auth routes in our app
  from .auth import auth as auth_blueprint
  app.register_blueprint(auth_blueprint)

  # blueprint for non-auth parts of app
  from .main import main as main_blueprint
  app.register_blueprint(main_blueprint)

  return(app)
