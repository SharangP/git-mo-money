import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
#from database import Database
#from flask.ext.login import LoginManager

app = Flask('GitMoMoney')
app.config.from_pyfile("config.py")
db = SQLAlchemy(app)
#login_manager = LoginManager()
#login_manager.setup_app(app)

import GitMoMoney.views
