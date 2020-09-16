from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

file_path = os.path.abspath(os.getcwd())+"/todo.db"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+file_path
db = SQLAlchemy(app)
