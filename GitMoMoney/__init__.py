from flask import Flask
#from database import Database
#from flask.ext.login import LoginManager

app = Flask('GitMoMoney')
#login_manager = LoginManager()
#login_manager.setup_app(app)
#database = Database(app)

import GitMoMoney.views
