import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
#from database import Database

app = Flask('GitMoMoney')
app.config.from_pyfile("config.py")
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.setup_app(app)

import GitMoMoney.views
