import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from config import basedir


app = Flask('GitMoMoney')
app.config.from_pyfile("config.py")
db = SQLAlchemy(app)

from GitMoMoney import views, models
