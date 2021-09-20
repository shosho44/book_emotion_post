# coding: UTF-8
import base64
import datetime
from flask import Flask, render_template, url_for, redirect, request
from flask_login import current_user, login_user, logout_user, login_required
import flask_login
from werkzeug.security import generate_password_hash, check_password_hash

import config
from model import models

app = config.app
DB  = config.DB


login_manager = flask_login.LoginManager()
login_manager.login_view = 'signin'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return DB.session.query(models.UserLoginInformation).filter_by(user_id=user_id).first()


@app.route('/', methods=['GET'])
@login_required
def show_main_page():
    if current_user.is_authenticated is False:
        return redirect(url_for('signin'))
    passages_information_table = DB.session.query(models.Passages, models.Users).join(models.Passages, models.Passages.user_id == models.Users.user_id)
    passages_information_list =  passages_information_table.order_by(models.Passages.created_at.desc()).all()
    current_user_id = current_user.user_id
    
    return render_template('index.html', passages_information_list=passages_information_list, current_user_id=current_user_id)


@app.route('/signin', methods=['GET'])
def signin():
    return render_template('signin.html')


@app.route('/signin-confirm', methods=['POST'])
def signin_confirm():
    user_id = request.form['user_id']
    password = request.form['password']
    
    print("\ninner signin-confirm")
    print("user_id, password: ", user_id, password)
    user = models.Users.query.filter_by(user_id=user_id).first()
    user_login_information = models.UserLoginInformation(user_id=user_id)
    
    if user is None or not check_password_hash(user.password, password):
        return redirect(url_for('signin'))

    print("user_login_information: ", user_login_information.user_id)
    
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

###############################################################################

# 投稿した時の処理
@app.route('/post-article', methods=['POST'])
def post_article():
    passage_content = request.form['post-article']
    book_title = request.form['book-title']
    
    user_id = current_user.user_id
    
    if book_title == '':
        book_title = '不明'
    
    insert_data = models.Passages(
        user_id=user_id,
        book_title=book_title,
        passage_content=passage_content,
        created_at=datetime.datetime.now()
    )
    
    DB.session.add(insert_data)
    DB.session.commit()
    
    return redirect(url_for('show_main_page'))


@app.route('/passage/<string:article_id>/delete', methods=['POST'])
def delete_passage(article_id=''):
    delete_passage_data = DB.session.query(PostArticle).filter_by(id=article_id).first()
    DB.session.delete(delete_passage_data)
    DB.session.commit()
    
    return redirect(url_for('show_main_page'))  # user-profileから投稿削除した時はuser-profileを返したい


@app.route('/user/<string:profile_user_id>', methods=['GET'])
def user_profile(profile_user_id=''):
    if current_user.is_authenticated is False:
        return redirect(url_for('signin'))
    
    user = models.Users.query.filter_by(user_id=profile_user_id).first()
    user_image = user.user_image.decode()
    
    current_user_id = current_user.user_id
    
    is_current_user_equal_article_user = False
    if current_user_id == profile_user_id:
        is_current_user_equal_article_user = True
        
    passages_information_list = models.Passages.query.filter_by(user_id=profile_user_id).order_by(models.Passages.created_at.desc()).all()
    if passages_information_list is None:
        passages_information_list = []
    
    return render_template('user-profile.html', user=user,
                            user_image=user_image, is_current_user_equal_article_user=is_current_user_equal_article_user,
                            some_article_data=passages_information_list)



# profile_user_idがcurrent_user_idと違う場合アクセス権限がない旨を表示する
@app.route('/user/<string:profile_user_id>/edit', methods=['GET'])
def edit_user_profile(profile_user_id=''):
    if current_user.is_authenticated is False:
        return redirect(url_for('signin'))
    
    user_id = current_user.user_id
    user_name = current_user.user_name  # 直す必要あり
    self_introduction = UserInformation.query.filter_by(user_id=user_id).first().self_introduction
    user_image = UserInformation.query.filter_by(user_id=user_id).first().user_image.decode()
    
    return render_template('edit-user-profile.html', user_id=user_id, user_name=user_name, self_introduction=self_introduction, user_image=user_image)


# user_profileに関係している
@app.route('/user/<string:profile_user_id>/update', methods=['POST'])
@login_required
def update_user_profile(profile_user_id=''):
    user_id = current_user.user_id
    user_name = request.form['user_name']
    self_introduction = request.form['self_introduction']
    
    user = DB.session.query(UserInformation).filter(UserInformation.user_id == user_id).first()
    user.user_name = user_name
    user.self_introduction = self_introduction
    
    DB.session.commit()
    
    return redirect(url_for('user_profile', profile_user_id=user_id))


# profile_user_idがcurrent_user_idと違う場合アクセス権限がない旨を表示する
@app.route('/user/<string:profile_user_id>/edit/image/upload', methods=['POST'])
@login_required
def upload_user_image(profile_user_id=''):
    current_user_id = current_user.user_id
    if 'user_image' not in request.files:
        return redirect(url_for('/user/{}/edit'.format(current_user_id)))
    
    user_image = request.files['user_image'].stream.read()
    user_image_base64 = base64.b64encode(user_image)
    
    user = DB.session.query(UserInformation).filter(UserInformation.user_id == current_user.user_id).first()
    user.user_image = user_image_base64
    
    DB.session.commit()  # 変更するかも。今の段階ではデータベースに登録する必要なしかも
    
    return redirect(url_for('user_profile', profile_user_id=profile_user_id))


# アクセス権限がない旨を表示する
@app.route('/user/<string:profile_user_id>/edit/image', methods=['GET'])
def show_upload_user_image(profile_user_id=''):
    if current_user.is_authenticated is False:
        return redirect(url_for('signin'))
    
    current_user_id = current_user.user_id
    
    return render_template('upload-user-image.html', user_id=current_user_id)


@app.route('/logout', methods=['GET'])
def logout_confirm():
    if current_user.is_authenticated is False:
        return redirect(url_for('signin'))
    
    user_id = current_user.user_id
    return render_template('logout-confirm.html', user_id=user_id)


@app.route('/run-logout', methods=['POST'])
@login_required
def run_logout():  # signinのURLに飛ぶときはログアウトする処理を書けばこの関数をなくして一つにまとめられるかもしれない
    logout_user()
    return redirect(url_for('signin'))


@app.route('/submit-reply/<string:article_id>', methods=['POST'])
def submit_reply(article_id=''):
    reply_content = request.form['reply_content']
    
    reply_user_name = UserInformation.query.filter_by(user_id=current_user.user_id).first().user_name
    
    reply_information = ReplyInformation(article_id=article_id, reply_user_id=current_user.user_id,
                                         reply_user_name=reply_user_name, reply_content=reply_content, created_at=time.time())
    
    DB.session.add(reply_information)
    DB.session.commit()
    return redirect(url_for('reply_thread', article_id=article_id))


@app.route('/reply/<string:article_id>', methods=['GET'])
def reply_thread(article_id=''):
    if current_user.is_authenticated is False:
        return redirect(url_for('signin'))
    
    current_user_id = current_user.user_id
    
    article_data = PostArticle.query.filter_by(id=article_id).first()
    
    some_reply_data = ReplyInformation.query.filter_by(article_id=article_id).order_by(ReplyInformation.created_at.desc()).all()
    
    if article_data:
        return render_template('reply_thread.html', article_data=article_data, some_reply_data=some_reply_data, current_user_id=current_user_id)
    else:
        return render_template('reply_thread.html', article_data=article_data)


@app.route('/passage/<string:article_id>/push-like', methods=['POST'])
def push_good_button(article_id=''):
    article = PostArticle.query.filter_by(id=article_id).first()
    user_id_push_good_button = current_user.user_id
    
    is_user_already_push_good_button = UserAndPushedGoodButtonArticle.query.filter_by(
        user_id_push_good_article=user_id_push_good_button, article_id=article_id).first()
    if is_user_already_push_good_button:
        article.good_sum -= 1
        
        delete_information_of_user_and_pushed_good_button_article = DB.session.query(UserAndPushedGoodButtonArticle).filter_by(
            user_id_push_good_article=user_id_push_good_button, article_id=article_id).first()
        DB.session.delete(delete_information_of_user_and_pushed_good_button_article)
        DB.session.commit()
        
        return redirect(url_for('show_main_page'))
    
    article.good_sum += 1
    
    user_and_pushed_good_button_article = UserAndPushedGoodButtonArticle(user_id_push_good_article=user_id_push_good_button, article_id=article_id)
    
    DB.session.add(user_and_pushed_good_button_article)
    DB.session.commit()
    
    return redirect(url_for('show_main_page'))


@app.route('/passage/<string:article_id>/likes', methods=['GET'])
def show_user_push_good(article_id=''):
    if current_user.is_authenticated is False:
        return redirect(url_for('signin'))
    
    some_user_push_good_information = UserAndPushedGoodButtonArticle.query.filter_by(article_id=article_id).all()
    
    return render_template('show-user-id-push-good.html', some_user_push_good_information=some_user_push_good_information)


# /push-good-button-reply
@app.route('/reply/<string:reply_id>/push-like/<string:article_id>', methods=['POST'])
def push_good_button_reply(reply_id='', article_id=''):
    reply = ReplyInformation.query.filter_by(id=reply_id).first()
    
    user_id_push_good_button = current_user.user_id
    
    is_user_already_push_good_button = UserAndPushedGoodButtonReply.query.filter_by(user_id_push_good_reply=user_id_push_good_button,
                                                                                    article_id=reply_id).first()
    if is_user_already_push_good_button:
        reply.good_sum -= 1
        
        delete_information_of_user_and_pushed_good_button_reply = DB.session.query(UserAndPushedGoodButtonReply).filter_by(
            user_id_push_good_reply=user_id_push_good_button, article_id=reply_id).first()
        DB.session.delete(delete_information_of_user_and_pushed_good_button_reply)
        DB.session.commit()
        
        return redirect(url_for('reply_thread', article_id=article_id))
    
    reply.good_sum += 1
    
    user_and_pushed_good_button_article = UserAndPushedGoodButtonReply(user_id_push_good_reply=user_id_push_good_button, article_id=reply_id)
    
    DB.session.add(user_and_pushed_good_button_article)
    DB.session.commit()
    
    return redirect(url_for('reply_thread', article_id=article_id))


@app.route('/reply/<string:article_id>/likes', methods=['GET'])
def show_user_push_good_reply(article_id=''):
    if current_user.is_authenticated is False:
        return redirect(url_for('signin'))
    
    some_user_push_good_information = UserAndPushedGoodButtonReply.query.filter_by(article_id=article_id).all()
    
    return render_template('show-user-id-push-good-reply.html', some_user_push_good_information=some_user_push_good_information)


# delete-reply
@app.route('/reply/<string:reply_id>/delete/<article_id>', methods=['POST'])
def delete_article_from_user_profile_reply(reply_id='', article_id=''):
    id = reply_id
    
    delete_reply_data = DB.session.query(ReplyInformation).filter_by(id=id).first()
    DB.session.delete(delete_reply_data)
    DB.session.commit()
    
    return redirect(url_for('reply_thread', article_id=article_id))


@app.route('/reply-to-reply/<string:id>', methods=['GET'])
def reply_to_reply(id=''):
    if current_user.is_authenticated is False:
        return redirect(url_for('signin'))
    
    current_user_id = current_user.user_id
    
    article_data = ReplyInformation.query.filter_by(id=id).first()
    
    some_reply_data = ReplyInformation.query.filter_by(reply_to_reply_article_id=id).order_by(ReplyInformation.created_at.desc()).all()
    
    if article_data:
        return render_template('reply_to_reply_thread.html', article_data=article_data, some_reply_data=some_reply_data,
                               current_user_id=current_user_id)
    else:
        return render_template('reply_to_reply_thread.html', article_data=article_data)


@app.route('/submit-reply-to-reply/<string:reply_to_reply_article_id>', methods=['POST'])
def submit_reply_to_reply(reply_to_reply_article_id=''):
    reply_content = request.form['reply_content']
    
    reply_user_name = UserInformation.query.filter_by(user_id=current_user.user_id).first().user_name
    
    reply_information = ReplyInformation(reply_to_reply_article_id=reply_to_reply_article_id, reply_user_id=current_user.user_id,
                                         reply_user_name=reply_user_name, reply_content=reply_content, created_at=time.time())
    
    DB.session.add(reply_information)
    DB.session.commit()
    
    return redirect(url_for('reply_to_reply', id=reply_to_reply_article_id))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
    DB.drop_all()
    DB.create_all()