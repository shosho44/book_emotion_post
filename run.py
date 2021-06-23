import hashlib

import flask
from flask import Flask, Response, abort, render_template, url_for, flash, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin
from collections import defaultdict
from flask_login import login_user
import flask_login

app = flask.Flask(__name__)

# データベースの設定
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.test'  # sqliteを使っている
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class PostArticle(db.Model):
    
    __tablename__ = 'articles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(128), nullable=False)
    post_content = db.Column(db.String(128), nullable=False)


class UserInformation(db.Model):
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    user_name = db.Column(db.String(128), nullable=False)
    email_address = db.Column(db.String(128), nullable=False)


@app.route('/', methods=['GET', 'POST'])  # index関数を実行している
def start_exe():
    return render_template('index.html')


users = UserInformation.query.all()
for user in users:
    print('\n\n')
    print(user.password)

"""
app.secret_key = 'secret key'

login_manager = flask_login.LoginManager()


# ログインする際に必要なユーザの情報
class User(flask_login.UserMixin):
    def __init__(self, user_id, user_password):
        self.user_id = user_id
        self.user_password = user_password
    
    def get_id(self):
        return self.user_id


# login
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'secret'


# ログインが必要なページに行くたびに実行される.セッションからユーザーをリロードする。
# 認証ユーザの呼び出し方を定義しているらしい
@login_manager.user_loader
def load_user(user_id):
    if user_id not in users:
        return
    
    user = User()
    user.user_id = user_id
    return user


# flaskのrequestからユーザをロードする.多分一番初めのログイン時に必要なんやと思う
@login_manager.request_loader
def request_loader(request):
    user_id = request.form.get('user_id')
    if user_id not in users:
        return
    
    user = User()
    user.user_id = user_id
    return user
"""


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    return render_template('signup.html')


@app.route('/article_redirect', methods=['GET', 'POST'])
def post_article_redirect():
    some_data = PostArticle.query.all()
    return render_template('index.html', some_data=some_data)


# 投稿した時の処理
@app.route('/post_article', methods=['POST'])
def post_article():
    post_content = request.form['post-article']
    tmp_user_id = '1'
    some_data = PostArticle(user_id=tmp_user_id, post_content=post_content)
    db.session.add(some_data)
    db.session.commit()
    return redirect(url_for('post_article_redirect'))  # 関数名を書く


@app.route('/signup_confirm', methods=['POST'])
def signup_confirm():
    user_id = request.form['user_id']
    user_name = request.form['user_name']
    email_address = request.form['email_address']
    password = hashlib.sha256(request.form['password'].encode('utf-8')).hexdigest()
    
    user_information = UserInformation(user_id=user_id, password=password, user_name=user_name, email_address=email_address)
    db.session.add(user_information)
    db.session.commit()
    return redirect(url_for('post_article_redirect'))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
    db.create_all()
