import flask
from flask import Flask, Response, abort, render_template, url_for, flash, redirect
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin
from collections import defaultdict
from flask_login import login_user
import flask_login

app = flask.Flask(__name__)
app.secret_key = 'secret key'

login_manager = flask_login.LoginManager()

# 登録されたユーザーの情報
users = {
    'shotaro_id1': {'password': 'shosho'},
    'shotaro_id2': {'password': 'shosho'},
    'shotaro_id3': {'password': 'shosho'},
    'shotaro_id4': {'password': 'shosho'},
    'shotaro_id5': {'password': 'shosho'},
    'shotaro_id6': {'password': 'shosho'},
    'shotaro_id7': {'password': 'shosho'},
    'shotaro_id8': {'password': 'shosho'},
    'shotaro_id9': {'password': 'shosho'},
    'shotaro_id10': {'password': 'shosho'},
    'shotaro_id11': {'password': 'shosho'},
    'shotaro_id12': {'password': 'shosho'}
}


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


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)