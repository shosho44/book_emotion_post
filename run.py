# coding: UTF-8
import base64
import time
from flask import Flask, render_template, url_for, redirect, request
from flask_login import current_user, login_user, logout_user, login_required
import flask_login
from werkzeug.security import generate_password_hash, check_password_hash

import config
from model import models

app = config.app
DB  = config.DB


login_manager = flask_login.LoginManager()
login_manager.login_view = 'signin'  # 参考URL:https://teratail.com/questions/167338
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return DB.session.query(models.UserLoginInformation).filter(user_id == user_id).first()


@app.route('/', methods=['GET'])
@login_required
def show_main_page():
    if current_user.is_authenticated is False:
        return redirect(url_for('signin'))
    
    some_data = models.Passages.query.order_by(models.Passages.created_at.desc()).all()
    current_user_id = current_user.user_id
    return render_template('index.html', some_data=some_data, current_user_id=current_user_id)


@app.route('/signin', methods=['GET'])
def signin():
    return render_template('signin.html')


@app.route('/signin-confirm', methods=['POST'])
def signin_confirm():
    user_id = request.form['user_id']
    password = request.form['password']
    
    user = models.Users.query.filter_by(user_id=user_id).first()
    user_login_information = models.UserLoginInformation(user_id=user_id)
    
    if user is None or not check_password_hash(user.password, password):
        return redirect(url_for('signin'))

    login_user(user_login_information)
    return redirect(url_for('show_main_page'))


@app.route('/signup', methods=['GET'])
def signup():
    return render_template('signup.html')


@app.route('/signup-confirm', methods=['POST'])
def signup_confirm():
    user_id = request.form['user_id']
    user_name = request.form['user_name']
    email_address = request.form['email_address']
    password = request.form['password']
    
    is_user_exist = models.Users.query.filter_by(email_address=email_address).first()
    if is_user_exist:
        return redirect(url_for('signup'))
    
    user = models.Users(user_id=user_id, password=generate_password_hash(password, method='sha256'),
                        user_name=user_name, email_address=email_address)
    user_login_information = models.UserLoginInformation(user_id=user_id)
    DB.session.add(user)
    DB.session.add(user_login_information)
    DB.session.commit()
    
    login_user(user_login_information)
    
    return redirect(url_for('show_main_page'))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
    DB.drop_all()
    DB.create_all()
