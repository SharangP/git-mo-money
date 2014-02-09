import os

DEBUG = True
GITHUB_KEY = '1f2a8e7b60a6f2b2e3f6d63a91da42b97ed9735e'
basedir = os.path.abspath(os.path.dirname(__file__))
SECRET_KEY = 'secret_key'

#SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test.db'
