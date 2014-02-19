import os

DEBUG = True
GITHUB_KEY = 'eab218628f745d68841af33a9e5e8e4e64bc45ec'
basedir = os.path.abspath(os.path.dirname(__file__))
SECRET_KEY = 'secret_key'

#SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test.db'
