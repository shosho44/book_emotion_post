import hashlib

import flask
from flask import Flask, Response, abort, render_template, url_for, flash, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user, login_user, logout_user, login_required, UserMixin
from collections import defaultdict
from flask_login import login_user
import flask_login
from werkzeug.security import generate_password_hash, check_password_hash


app = flask.Flask(__name__)

# データベースの設定
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.test'  # sqliteを使っている
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class PostArticle(db.Model):
    
    __tablename__ = 'articles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(128), nullable=False)
    user_name = db.Column(db.String(128), nullable=False)
    book_title = db.Column(db.String(128), nullable=True)
    post_content = db.Column(db.String(128), nullable=False)


class UserInformation(UserMixin, db.Model):
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    user_name = db.Column(db.String(128), nullable=False)
    email_address = db.Column(db.String(128), nullable=False)


app.secret_key = 'secret key'  # セッションを有効にするために必要
app.config['SECRET_KEY'] = 'secret'

login_manager = flask_login.LoginManager()
login_manager.login_view = 'signin'  # 参考URL:https://teratail.com/questions/167338
login_manager.init_app(app)


# ログインが必要なページに行くたびに実行される.セッションからユーザーをリロードする。
# 認証ユーザの呼び出し方を定義しているらしい
@login_manager.user_loader
def load_user(user_id):
    return UserInformation.query.get(user_id)


@app.route('/', methods=['GET', 'POST'])  # index関数を実行している
def start_exe():
    some_data = PostArticle.query.all()
    return render_template('index.html', some_data=some_data)


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    return render_template('signin.html')


@app.route('/signin_confirm', methods=['GET', 'POST'])
def signin_confirm():
    user_id = request.form['user_id']
    password = request.form['password']
    
    users = UserInformation
    is_user = users.query.filter_by(user_id=user_id).first()
    
    if is_user is None or not check_password_hash(is_user.password, password):
        return redirect(url_for('signin'))
    else:
        user = is_user
        login_user(user)
        return redirect(url_for('start_exe'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    return render_template('signup.html')


@app.route('/index', methods=['GET', 'POST'])
def post_article_redirect():
    some_data = PostArticle.query.all()
    return render_template('index.html', some_data=some_data)


# 投稿した時の処理
@app.route('/post_article', methods=['POST'])
def post_article():
    post_content = request.form['post-article']
    book_title = request.form['book-title']
    
    user_id = current_user.user_id
    
    is_post_user_name = UserInformation.query.filter_by(user_id=user_id).first()
    if is_post_user_name is None:
        user_name = 'unknown_user'
    else:
        user_name = is_post_user_name.user_name
    
    some_data = PostArticle(user_id=user_id, user_name=user_name, book_title=book_title, post_content=post_content)
    
    db.session.add(some_data)
    db.session.commit()
    return redirect(url_for('post_article_redirect'))  # 関数名を書く


@app.route('/signup_confirm', methods=['POST'])
def signup_confirm():
    user_id = request.form['user_id']
    user_name = request.form['user_name']
    email_address = request.form['email_address']
    password = request.form['password']
    
    is_user_exist = UserInformation.query.filter_by(email_address=email_address).first()
    if is_user_exist:
        return redirect(url_for('signup'))  # リダイレクト先変更する
    
    user_information = UserInformation(user_id=user_id, password=generate_password_hash(password, method='sha256'), user_name=user_name, email_address=email_address)
    db.session.add(user_information)
    db.session.commit()
    return redirect(url_for('post_article_redirect'))


@app.route('/user_profile', methods=['POST', 'GET'])
def user_profile():
    user_id = current_user.user_id
    user_name = current_user.user_name
    
    is_article_exist = PostArticle.query.filter_by(user_id=user_id).all()
    
    if is_article_exist:
        some_article_data = is_article_exist
        return render_template('user-profile.html', user_id=user_id, user_name=user_name, some_article_data=some_article_data)
    else:
        return render_template('user-profile.html', user_id=user_id, user_name=user_name)


@app.route('/logout_confirm', methods=['POST'])
@login_required
def logout_confirm():
    return render_template('logout-confirm.html')


@app.route('/logout_no', methods=['POST'])
@login_required
def logout_no():
    return redirect(url_for('user_profile'))


@app.route('/logout_yes', methods=['POST'])
@login_required
def logout_yes():
    logout_user()
    return redirect(url_for('signin'))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
    db.create_all()
