from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'

#blueprint for auth routes
from app.auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

#blueprint dor non-auth parts of app
from app.main import main as main_blueprint
app.register_blueprint(main_blueprint)
