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
    
    passages_information_table = DB.session.query(models.Passages) \
                                                  .filter(models.Passages.user_id == models.Users.user_id) \
                                                  .filter(models.Passages.passage_id == models.PostIDs.passage_id)
    
    passages_information_list =  passages_information_table.order_by(models.Passages.created_at.desc()).all()
    current_user_id = current_user.user_id
    
    return render_template('main-page.html',
                           passages_information_list=passages_information_list,
                           user_id=current_user_id
                           )


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
    
    insert_user_data = models.Users(
        user_id=user_id,
        password=generate_password_hash(password, method='sha256'),
        user_name=user_name,
        email_address=email_address,
        created_at=datetime.datetime.now()
    )
    
    insert_user_login_information_data = models.UserLoginInformation(user_id=user_id)
    
    DB.session.add(insert_user_data)
    DB.session.add(insert_user_login_information_data)
    DB.session.commit()
    
    login_user(insert_user_login_information_data)
    
    return redirect(url_for('show_main_page'))


@app.route('/post-passage', methods=['POST'])
def post_passage():
    passage_content = request.form['passage_content']
    book_title = request.form['book_title']
    
    current_user_id = current_user.user_id
    
    if book_title == '':
        book_title = '不明'
    
    insert_passage_data = models.Passages(
        user_id=current_user_id,
        book_title=book_title,
        passage_content=passage_content,
        created_at=datetime.datetime.now()
    )
    
    DB.session.add(insert_passage_data)
    DB.session.commit()
    
    insert_post_IDs_data = models.PostIDs(passage_id=insert_passage_data.passage_id)
    
    DB.session.add(insert_post_IDs_data)
    DB.session.commit()
    
    insert_passage_coments_relations_data = models.PassageCommentRelations(parent_id=insert_post_IDs_data.post_id)
    
    DB.session.add(insert_passage_coments_relations_data)
    DB.session.commit()
    
    print("\n\ninsert_passage_data: ", insert_passage_data.passage_id)
    return redirect(url_for('show_main_page'))


@app.route('/passage/<string:passage_id>/delete', methods=['POST'])
def delete_passage(passage_id=''):
    post_id = models.PostIDs.query.filter_by(passage_id=passage_id).first().post_id
    
    models.PassageCommentRelations.query.filter_by(parent_id=post_id).delete()
    models.PassageCommentRelations.query.filter_by(child_id=post_id).delete()
    models.PassageLikes.query.filter_by(passage_id=passage_id).delete()
    models.PassageLikes.query.filter_by(passage_id=passage_id).delete()
    
    delete_passage_data = DB.session.query(models.Passages).filter_by(passage_id=passage_id).first()
    delete_post_IDs_data = models.PostIDs.query.filter_by(passage_id=passage_id).first()
    
    DB.session.delete(delete_passage_data)
    DB.session.delete(delete_post_IDs_data)
    DB.session.commit()
    
    return redirect(url_for('show_main_page'))  # user-profileから投稿削除した時はuser-profileを返したいtodo


@app.route('/passage/<string:passage_id>/push-like', methods=['POST'])
def push_good_button(passage_id=''):
    current_user_id = current_user.user_id
    
    has_user_already_push_liked = models.PassageLikes.query.filter_by(passage_id=passage_id, user_id=current_user_id).first()
    
    if has_user_already_push_liked:
        insert_data = models.PassageLikes(
            user_id=current_user_id,
            passage_id=passage_id,
            created_at=datetime.datetime.now()
        )

        DB.session.add(insert_data)
        DB.session.commit()
    else:
        delete_data = has_user_already_push_liked
        DB.session.add(delete_data)
        DB.session.commit()
    
    return redirect(url_for('show_main_page'))


@app.route('/passage/<string:passage_id>/likes', methods=['GET'])
def show_user_push_good(passage_id=''):
    if current_user.is_authenticated is False:
        return redirect(url_for('signin'))
    
    passage_likes_data_list = models.PassageLikes.query.filter_by(passage_id=passage_id).all()
    
    return render_template('user-id-push-like.html',
                           passage_likes_data_list=passage_likes_data_list
                           )


@app.route('/user/<string:user_id>', methods=['GET'])
def user_profile(user_id=''):
    if current_user.is_authenticated is False:
        return redirect(url_for('signin'))
    
    user = models.Users.query.filter_by(user_id=user_id).first()
    user_image = user.user_image.decode()
    
    current_user_id = current_user.user_id
    
    is_current_user_equal_profile_user = False
    if current_user_id == user_id:
        is_current_user_equal_profile_user = True
        
    passages_data_list = models.Passages.query.filter_by(user_id=user_id).order_by(models.Passages.created_at.desc()).all()
    if passages_data_list is None:
        passages_data_list = []
    
    return render_template('user-profile.html',
                           user=user,
                           user_image=user_image,
                           is_current_user_equal_profile_user=is_current_user_equal_profile_user,
                           passages_data_list=passages_data_list
                           )  #  good_sumに変わるいいね数を算出する処理を行うlike_sumという変数に入れるTodo


@app.route('/user/<string:user_id>/edit', methods=['GET'])
def edit_user_profile(user_id=''):
    current_user_id = current_user.user_id
    if current_user_id != user_id:
        return redirect(url_for('user_profile',
                                user_id=user_id
                                )
                        )
    
    user = models.Users.query.filter_by(user_id=user_id).first()
    user_image = user.user_image.decode()
    return render_template('edit-user-profile.html',
                           user_id=user_id,
                           user_image=user_image
                           )


@app.route('/user/<string:user_id>/update', methods=['POST'])
def update_user_profile(user_id=''):
    user_name = request.form['user_name']
    self_introduction = request.form['self_introduction']
    
    user = models.Users.query.filter_by(user_id=user_id).first()
    user.user_name = user_name
    user.self_introduction = self_introduction
    
    DB.session.commit()
    
    return redirect(url_for('user_profile',
                            user_id=user_id
                            )
                    )


@app.route('/user/<string:user_id>/edit/image/upload', methods=['POST'])
def upload_user_image(user_id=''):
    if 'user_image' not in request.files:
        return redirect(url_for('/user/{}/edit'.format(user_id)))
    
    user_image = request.files['user_image'].stream.read()
    user_image_base64 = base64.b64encode(user_image)
    
    user = models.Users.query.filter_by(user_id=user_id).first()
    user.user_image = user_image_base64
    
    DB.session.commit()
    
    return redirect(url_for('user_profile',
                            user_id=user_id
                            )
                    )


@app.route('/user/<string:user_id>/edit/image', methods=['GET'])
def show_edit_user_image(user_id=''):
    current_user_id = current_user.user_id
    if user_id != current_user_id:
        return redirect(url_for('user_profile',
                                user_id=user_id
                                )
                        )
    
    return render_template('edit-user-image.html',
                           user_id=user_id
                           )


@app.route('/logout', methods=['GET'])
def show_logout():
    current_user_id = current_user.user_id
    
    return render_template('logout-confirm.html',
                           user_id=current_user_id
                           )  # mainページからの場合はメインに返す


@app.route('/run-logout', methods=['POST'])
def run_logout():
    logout_user()
    
    return redirect(url_for('signin'))


"""
# 実装途中
@app.route('/posts/<int:post_id>', methods=['GET'])
def show_posts(post_id):
    passage_id = models.PostIDs.query.filter_by(post_id=post_id).first().passage_id
    passage_data = models.Passages.query.filter_by(passage_id=passage_id).first()
    
    child_data_list = DB.session.query(models.Comments) \
                                .filter(models.Comments.comment_id == models.PostIDs.comment_id) \
                                .filter(models.PostIDs.post_id == models.PassageCommentRelations.child_id) \
                                .filter_by(parent_id = passage_id).all()
    
    if passage_id == -1:
        pass
        # comment_id = models.PostIDs.query.filter_by(post_id=post_id).first().comment_id
        # comment_data = models.Comments.query.filter_by(comment_id=comment_id).first()
    
    return render_template('posts-thread.html',
                           passage_data=passage_data,
                           child_data_list=child_data_list,
                           current_user_id = current_user.user_id
                           )  #  good_sumに変わるいいね数を算出する処理を行うlike_sumという変数に入れるTodo
"""

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
    DB.drop_all()
    DB.create_all()