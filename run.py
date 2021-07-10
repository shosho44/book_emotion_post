# coding: UTF-8
import base64
import hashlib
from logging import exception
import time

import flask
from flask import Flask, Response, abort, render_template, url_for, flash, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user, login_user, logout_user, login_required, UserMixin
from collections import defaultdict
from flask_login import login_user
import flask_login
from werkzeug.security import generate_password_hash, check_password_hash

app = flask.Flask(__name__, static_folder='img')

# データベースの設定
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db'  # sqliteを使っている
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

with open('img/sample_image_human.png', mode='rb') as f:
    default_user_image_base64 = base64.b64encode(f.read())


class PostArticle(db.Model):
    
    __tablename__ = 'articles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(128), nullable=False)
    user_name = db.Column(db.String(128), nullable=False)
    book_title = db.Column(db.String(128), nullable=False, default='不明')
    post_content = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.Float, nullable=False)
    good_sum = db.Column(db.Integer, nullable=False, default=0)


class ReplyInformation(db.Model):
    
    __tablename__ = 'articlereply'
    
    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.String(128), nullable=False)
    reply_user_id = db.Column(db.String(128), nullable=False)
    reply_user_name = db.Column(db.String(128), nullable=False)
    reply_content = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.Float, nullable=False)
    good_sum = db.Column(db.Integer, nullable=False, default=0)


class UserInformation(UserMixin, db.Model):
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    user_name = db.Column(db.String(128), nullable=False)
    email_address = db.Column(db.String(128), nullable=False)
    self_introduction = db.Column(db.String(128), nullable=False, default='')
    user_image = db.Column(db.LargeBinary, nullable=False, default=default_user_image_base64)


class UserAndPushedGoodButtonArticle(db.Model):
    
    __tablename__ = 'user_and_pushed_good_button_article'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id_push_article = db.Column(db.String(128), nullable=False)
    article_id = db.Column(db.Integer, nullable=False)


app.secret_key = 'secret key'  # セッションを有効にするために必要
app.config['SECRET_KEY'] = 'secret'

login_manager = flask_login.LoginManager()
login_manager.login_view = 'signin'  # 参考URL:https://teratail.com/questions/167338
login_manager.init_app(app)


# ログインが必要なページに行くたびに実行される.セッションからユーザーをリロードする。
# 認証ユーザの呼び出し方を定義しているらしい
@login_manager.user_loader
def load_user(user_id):
    print('user_id:', user_id)
    print('\n\n')
    is_user_information_exist = UserInformation.query.get(user_id)
    if is_user_information_exist:
        return is_user_information_exist
    else:
        return ''


@app.route('/', methods=['GET', 'POST'])  # index関数を実行している
def start_exe():
    some_data = PostArticle.query.order_by(PostArticle.created_at.desc()).all()
    current_user_id = current_user.user_id
    return render_template('index.html', some_data=some_data, current_user_id=current_user_id)


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
    some_data = PostArticle.query.order_by(PostArticle.created_at.desc()).all()
    current_user_id = current_user.user_id
    return render_template('index.html', some_data=some_data, current_user_id=current_user_id)


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
    
    some_data = PostArticle(user_id=user_id, user_name=user_name, book_title=book_title, post_content=post_content, created_at=time.time())
    
    db.session.add(some_data)
    db.session.commit()
    return redirect(url_for('post_article_redirect'))  # 関数名を書く


@app.route('/delete_article_from_user_profile', methods=['GET', 'POST'])
def delete_article_from_user_profile():
    article_id = request.form['article_id']
    
    delete_article_data = db.session.query(PostArticle).filter_by(id=article_id).first()
    db.session.delete(delete_article_data)
    db.session.commit()
    
    return redirect(url_for('start_exe'))


@app.route('/delete_article_from_home', methods=['GET', 'POST'])
def delete_article_from_home():
    article_id = request.form['article_id']
    
    delete_article_data = db.session.query(PostArticle).filter_by(id=article_id).first()
    db.session.delete(delete_article_data)
    db.session.commit()
    
    return redirect(url_for('start_exe'))


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
    
    user = user_information
    login_user(user)
    return redirect(url_for('post_article_redirect'))


@app.route('/user_profile', methods=['POST', 'GET'])
def user_profile():
    user_id = current_user.user_id
    if 'user_id' in request.form:
        user_id = request.form['user_id']
    
    user = UserInformation.query.filter_by(user_id=user_id).first()
    user_name = user.user_name
    self_introduction = user.self_introduction
    user_image = user.user_image.decode()
    
    if current_user.user_id == user_id:
        is_current_user_equal_article_user = True
    else:
        is_current_user_equal_article_user = False
    
    is_article_exist = PostArticle.query.filter_by(user_id=user_id).all()
    
    if is_article_exist:
        some_article_data = is_article_exist
        return render_template('user-profile.html', user_id=user_id, user_name=user_name, self_introduction=self_introduction,
                               user_image=user_image, is_current_user_equal_article_user=is_current_user_equal_article_user,
                               some_article_data=some_article_data)
    else:
        return render_template('user-profile.html', user_id=user_id, user_name=user_name, self_introduction=self_introduction,
                               user_image=user_image, is_current_user_equal_article_user=is_current_user_equal_article_user)


@app.route('/edit_user_profile', methods=['POST', 'GET'])
def edit_user_profile():
    user_id = current_user.user_id
    user_name = current_user.user_name
    self_introduction = UserInformation.query.filter_by(user_id=user_id).first().self_introduction
    user_image = UserInformation.query.filter_by(user_id=user_id).first().user_image.decode()
    
    return render_template('edit-user-profile.html', user_id=user_id, user_name=user_name, self_introduction=self_introduction, user_image=user_image)


@app.route('/update_user_profile', methods=['POST', 'GET'])
@login_required
def update_user_profile():
    user_id = current_user.user_id
    user_name = request.form['user_name']
    self_introduction = request.form['self_introduction']
    
    user = db.session.query(UserInformation).filter(UserInformation.user_id == user_id).first()
    user.user_name = user_name
    user.self_introduction = self_introduction
    
    db.session.commit()
    
    return redirect(url_for('user_profile'))


@app.route('/upload_user_image', methods=['GET', 'POST'])
@login_required
def upload_user_image():
    if 'user_image' not in request.files:
        return redirect(url_for('edit_user_profile'))
    
    user_image = request.files['user_image'].stream.read()
    user_image_base64 = base64.b64encode(user_image)
    
    user = db.session.query(UserInformation).filter(UserInformation.user_id == current_user.user_id).first()
    user.user_image = user_image_base64
    
    db.session.commit()  # 変更するかも。今の段階ではデータベースに登録する必要なしかも
    
    return redirect(url_for('edit_user_profile'))


@app.route('/show_upload_user_image', methods=['GET', 'POST'])
def show_upload_user_image():
    return render_template('upload-user-image.html')


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


@app.route('/submit_reply', methods=['POST'])
def submit_reply():
    reply_content = request.form['reply_content']
    article_id = request.form['article_id']
    
    reply_user_name = UserInformation.query.filter_by(user_id=current_user.user_id).first().user_name
    
    reply_information = ReplyInformation(article_id=article_id, reply_user_id=current_user.user_id, reply_user_name=reply_user_name, reply_content=reply_content, created_at=time.time())
    
    db.session.add(reply_information)
    db.session.commit()
    return reply_thread(article_id)


@app.route('/reply_thread', methods=['GET', 'POST'])
def reply_thread(article_id=''):
    if 'article_id' in request.form:
        article_id = request.form['article_id']
    
    article_data = PostArticle.query.filter_by(id=article_id).first()
    
    some_reply_data = ReplyInformation.query.filter_by(article_id=article_id).order_by(ReplyInformation.created_at.desc()).all()
    
    if article_data:
        return render_template('reply_thread.html', article_data=article_data, some_reply_data=some_reply_data)
    else:
        return render_template('reply_thread.html', article_data=article_data)


@app.route('/push_good_button', methods=['POST'])
def push_good_button():
    article_id = request.form['article_id']
    
    article = PostArticle.query.filter_by(id=article_id).first()
    
    user_id_push_good_button = current_user.user_id
    
    is_user_already_push_good_button = UserAndPushedGoodButtonArticle.query.filter_by(user_id_push_article=user_id_push_good_button, article_id=article_id).first()
    if is_user_already_push_good_button:
        article.good_sum -= 1
        
        delete_information_of_user_and_pushed_good_button_article = db.session.query(UserAndPushedGoodButtonArticle).filter_by(user_id_push_article=user_id_push_good_button, article_id=article_id).first()
        db.session.delete(delete_information_of_user_and_pushed_good_button_article)
        db.session.commit()
        
        return redirect(url_for('start_exe'))
    
    article.good_sum += 1
    
    user_and_pushed_good_button_article = UserAndPushedGoodButtonArticle(user_id_push_article=user_id_push_good_button, article_id=article_id)
    
    db.session.add(user_and_pushed_good_button_article)
    db.session.commit()
    
    return redirect(url_for('start_exe'))


@app.route('/show_user_push_good', methods=['GET', 'POST'])
def show_user_push_good():
    article_id = request.form['article_id']
    some_user_push_good_information = UserAndPushedGoodButtonArticle.query.filter_by(article_id=article_id).all()
    
    return render_template('show-user-id-push-good.html', some_user_push_good_information=some_user_push_good_information)
    
    
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
    db.create_all()
