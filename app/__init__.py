from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os 
app = Flask(__name__)
# config for forms 

# this key should not be in souce code for production
app.config['SECRET_KEY'] = 'secret321'

# config for db
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

from app import routes