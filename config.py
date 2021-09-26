# coding: UTF-8
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_folder='static')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['APPLICATION_ROOT'] = '/'
app.secret_key = 'secret key'  # セッションを有効にするために必要
app.config['SECRET_KEY'] = 'secret'

DB = SQLAlchemy(app)