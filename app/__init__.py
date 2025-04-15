from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from app.config import SQLALCHEMY_DATABASE_URI, SECRET_KEY
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SECRET_KEY'] = SECRET_KEY

lm = LoginManager(app)
lm.login_view = 'login'
lm.login_message = "Пожалуйста, войдите, чтобы открыть эту страницу."
bootstrap = Bootstrap(app)

from app import models, routes