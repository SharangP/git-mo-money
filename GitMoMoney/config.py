import os

DEBUG = True
GITHUB_KEY = '346e8e420f7c16edd95d5d6cbc7a50f9fb8ab49e'
basedir = os.path.abspath(os.path.dirname(__file__))
SECRET_KEY = 'secret_key'

#SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test.db'
