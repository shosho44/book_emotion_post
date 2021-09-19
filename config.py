# coding: UTF-8
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_folder='static')

# データベースの設定
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db'  # sqliteを使っている
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['APPLICATION_ROOT'] = '/'
db = SQLAlchemy(app)

app.secret_key = 'secret key'  # セッションを有効にするために必要
app.config['SECRET_KEY'] = 'secret'