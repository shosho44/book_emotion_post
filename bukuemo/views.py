# coding: UTF-8
import base64
import datetime
from flask import Flask, render_template, url_for, redirect, request
from flask_login import current_user, login_user, logout_user, login_required
import flask_login
from werkzeug.security import generate_password_hash, check_password_hash
from cryptography.fernet import Fernet

from bukuemo.models import Comments, CommentLikes, Passages, PassageCommentRelations, PassageLikes, PostIDs, UserLoginInformation, Users
from bukuemo import app, db

login_manager = flask_login.LoginManager()
login_manager.login_view = 'signin'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(UserLoginInformation).filter_by(user_id=user_id).first()


@app.route('/', methods=['GET'])
@login_required
def show_main_page():
    if current_user.is_authenticated is False:
        return redirect(url_for('signin'))
    
    passages_information_table = db.session.query(Passages,
                                                  Users,
                                                  PostIDs
                                                  ).join(
                                                      Users,
                                                      Passages.user_id == Users.user_id
                                                      ).join(
                                                          PostIDs,
                                                          Passages.passage_id == PostIDs.passage_id
                                                      )
    
    passages_information_list = passages_information_table.order_by(Passages.created_at.desc()).all()
    current_user_id = current_user.user_id
    
    passage_like_sum_list = []
    
    for passages_information in passages_information_list:
        passage_like_sum = len(PassageLikes.query.filter_by(passage_id=passages_information.Passages.passage_id).all())
        
        passage_like_sum_list.append(passage_like_sum)
    
    return render_template('main-page.html',
                           ziped_list = zip(passages_information_list, passage_like_sum_list),
                           current_user_id=current_user_id
                           )


@app.route('/signin', methods=['GET'])
def signin():
    return render_template('signin.html')


@app.route('/signin-confirm', methods=['POST'])
def signin_confirm():
    user_id = request.form['user_id']
    password = request.form['password']
    
    user = Users.query.filter_by(user_id=user_id).first()
    
    user_login_information = UserLoginInformation(user_id=user_id)
    
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
    
    key = b'6NpAoIihGtar-gthg9eExg0yKFxBEHkvldg9epEkwg8='  # 変更する必要あり。環境変数に入れよう
    fernet = Fernet(key)
    encryptec_email_address = fernet.encrypt(email_address.encode())
    
    is_user_exist = Users.query.filter_by(email_address=encryptec_email_address).first()
    if is_user_exist or user_id == '' or user_name == '' or email_address == '' or password == '':
        return redirect(url_for('signup'))
    
    insert_user_data = Users(
        user_id=user_id,
        password=generate_password_hash(password, method='sha256'),
        user_name=user_name,
        email_address=encryptec_email_address,
        created_at=datetime.datetime.now()
    )
    
    insert_user_login_information_data = UserLoginInformation(user_id=user_id)
    
    db.session.add(insert_user_data)
    db.session.add(insert_user_login_information_data)
    db.session.commit()
    
    login_user(insert_user_login_information_data)
    
    return redirect(url_for('show_main_page'))


@app.route('/post-passage', methods=['POST'])
def post_passage():
    passage_content = request.form['passage_content']
    book_title = request.form['book_title']
    
    current_user_id = current_user.user_id
    
    if book_title == '':
        book_title = '不明'
    
    insert_passage_data = Passages(
        user_id=current_user_id,
        book_title=book_title,
        passage_content=passage_content,
        created_at=datetime.datetime.now()
    )
    
    db.session.add(insert_passage_data)
    db.session.commit()
    
    insert_post_IDs_data = PostIDs(passage_id=insert_passage_data.passage_id)
    
    db.session.add(insert_post_IDs_data)
    db.session.commit()
    
    insert_passage_coments_relations_data = PassageCommentRelations(parent_id=insert_post_IDs_data.post_id)
    
    db.session.add(insert_passage_coments_relations_data)
    db.session.commit()
    
    return redirect(url_for('show_main_page'))


@app.route('/passage/<string:passage_id>/delete', methods=['POST'])
def delete_passage(passage_id=''):
    post_id = PostIDs.query.filter_by(passage_id=passage_id).first().post_id
    
    PassageCommentRelations.query.filter_by(parent_id=post_id).delete()
    PassageCommentRelations.query.filter_by(child_id=post_id).delete()
    PassageLikes.query.filter_by(passage_id=passage_id).delete()
    
    delete_passage_data = db.session.query(Passages).filter_by(passage_id=passage_id).first()
    delete_post_IDs_data = PostIDs.query.filter_by(passage_id=passage_id).first()
    
    db.session.delete(delete_passage_data)
    db.session.delete(delete_post_IDs_data)
    db.session.commit()
    
    return redirect(url_for('show_main_page'))  # user-profileから投稿削除した時はuser-profileを返したいtodo


@app.route('/passage/<int:passage_id>/push-like/<int:parent_post_id>', methods=['POST'])
@app.route('/passage/<int:passage_id>/push-like', methods=['POST'])
def push_like_button_passage(passage_id, parent_post_id=-1):
    current_user_id = current_user.user_id
    
    has_user_already_push_liked = PassageLikes.query.filter_by(passage_id=passage_id, user_id=current_user_id).first()
    
    if has_user_already_push_liked is None:
        insert_data = PassageLikes(
            user_id=current_user_id,
            passage_id=passage_id,
            created_at=datetime.datetime.now()
        )

        db.session.add(insert_data)
        db.session.commit()
    else:
        delete_data = has_user_already_push_liked
        db.session.delete(delete_data)
        db.session.commit()
    
    if parent_post_id != -1:
        return redirect(url_for(
            'show_posts',
            post_id=parent_post_id
            )
                        )
    
    return redirect(url_for('show_main_page'))


@app.route('/post/<int:post_id>/likes', methods=['GET'])
def show_user_push_good(post_id):
    if current_user.is_authenticated is False:
        return redirect(url_for('signin'))
    
    current_user_id = current_user.user_id
    
    passage_id = PostIDs.query.filter_by(post_id=post_id).first().passage_id
    
    is_passage = True
    
    if passage_id == -1:
        is_passage = False
        comment_id = PostIDs.query.filter_by(post_id=post_id).first().comment_id
        
        post_likes_data_list = db.session.query(CommentLikes,
                                                Users
                                                ).join(
                                                    Users,
                                                    Users.user_id == CommentLikes.user_id
                                                ).filter(CommentLikes.comment_id==comment_id).all()
                                                
        return render_template('user-id-push-like.html',
                               post_likes_data_list=post_likes_data_list,
                               current_user_id=current_user_id,
                               is_passage=is_passage
                               )
    
    post_likes_data_list = db.session.query(PassageLikes,
                                            Users
                                            ).join(
                                                Users,
                                                Users.user_id == PassageLikes.user_id
                                            ).filter(PassageLikes.passage_id==passage_id).all()
    
    return render_template('user-id-push-like.html',
                           post_likes_data_list=post_likes_data_list,
                           current_user_id=current_user_id,
                           is_passage=is_passage
                           )


@app.route('/user/<string:user_id>', methods=['GET'])
def show_user_profile(user_id=''):
    if current_user.is_authenticated is False:
        return redirect(url_for('signin'))
    
    user = Users.query.filter_by(user_id=user_id).first()
    user_image = user.user_image.decode()
    
    current_user_id = current_user.user_id
    
    is_current_user_equal_profile_user = False
    if current_user_id == user_id:
        is_current_user_equal_profile_user = True
    
    passages_information_list = db.session.query(Passages,
                                          PostIDs
                                          ).join(
                                              PostIDs,
                                              Passages.passage_id == PostIDs.passage_id
                                              ).filter(Passages.user_id==user_id).order_by(Passages.created_at.desc()).all()

    if passages_information_list is None:
        passages_information_list = []
    
    passage_like_sum_list = []
    
    for passages_information in passages_information_list:
        passage_like_sum = len(PassageLikes.query.filter_by(passage_id=passages_information.Passages.passage_id).all())
        
        passage_like_sum_list.append(passage_like_sum)
        
    return render_template('user-profile.html',
                           user=user,
                           current_user_id=current_user.user_id,
                           user_image=user_image,
                           is_current_user_equal_profile_user=is_current_user_equal_profile_user,
                           ziped_passages_and_like_sum_data_list=zip(passages_information_list, passage_like_sum_list)
                           )  #  good_sumに変わるいいね数を算出する処理を行うlike_sumという変数に入れるTodo


@app.route('/user/<string:user_id>/edit', methods=['GET'])
def edit_user_profile(user_id=''):
    current_user_id = current_user.user_id
    if current_user_id != user_id:
        return redirect(url_for('show_user_profile',
                                user_id=user_id
                                )
                        )
    
    user = Users.query.filter_by(user_id=user_id).first()
    user_image = user.user_image.decode()
    return render_template('edit-user-profile.html',
                           current_user_id=user_id,
                           user_image=user_image
                           )


@app.route('/user/<string:user_id>/update', methods=['POST'])
def update_user_profile(user_id=''):
    user_name = request.form['user_name']
    self_introduction = request.form['self_introduction']
    
    user = Users.query.filter_by(user_id=user_id).first()
    user.user_name = user_name
    user.self_introduction = self_introduction
    
    db.session.commit()
    
    return redirect(url_for('show_user_profile',
                            user_id=user_id
                            )
                    )


@app.route('/user/<string:user_id>/edit/image/upload', methods=['POST'])
def upload_user_image(user_id=''):
    if 'user_image' not in request.files:
        return redirect(url_for('/user/{}/edit'.format(user_id)))
    
    user_image = request.files['user_image'].stream.read()
    user_image_base64 = base64.b64encode(user_image)
    
    user = Users.query.filter_by(user_id=user_id).first()
    user.user_image = user_image_base64
    
    db.session.commit()
    
    return redirect(url_for('show_user_profile',
                            user_id=user_id
                            )
                    )


@app.route('/user/<string:user_id>/edit/image', methods=['GET'])
def show_edit_user_image(user_id=''):
    current_user_id = current_user.user_id
    if user_id != current_user_id:
        return redirect(url_for('show_user_profile',
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
    print(current_user.is_authenticated)
    return redirect(url_for('signin'))


@app.route('/comment/<int:post_id>', methods=['GET'])
def show_posts(post_id):
    passage_id = PostIDs.query.filter_by(post_id=post_id).first().passage_id
    parent_post_id = post_id
    
    child_data_table = db.session.query(Comments,
                                        PassageCommentRelations,
                                        PostIDs,
                                        Users
                                        ).join(
                                            PostIDs,
                                            Comments.comment_id == PostIDs.comment_id
                                            ).join(
                                                PassageCommentRelations,
                                                PostIDs.post_id == PassageCommentRelations.child_id
                                            ).join(
                                                Users,
                                                Comments.user_id == Users.user_id
                                                )
    child_data_list = child_data_table.filter(PassageCommentRelations.parent_id == parent_post_id).order_by(Comments.created_at.desc()).all()
    
    child_like_sum_list = []
    
    for child_data in child_data_list:
        comment_like_sum = len(CommentLikes.query.filter_by(comment_id=child_data.Comments.comment_id).all())
        child_like_sum_list.append(comment_like_sum)
        
    if passage_id == -1:
        parent_content = parent_user_name = parent_user_id = ''
        is_passage = False
        
        comment_id = PostIDs.query.filter_by(post_id=post_id).first().comment_id
        
        comment_data = db.session.query(Comments,
                                        Users
                                        ).join(
                                            Users,
                                            Comments.user_id == Users.user_id
                                            ).filter(Comments.comment_id==comment_id).first()
        
        parent_content = comment_data.Comments.comment_content
        parent_user_id = comment_data.Users.user_id
        parent_user_name = comment_data.Users.user_name
        parent_like_sum = len(CommentLikes.query.filter(CommentLikes.comment_id==comment_id).all())
        
        
        return render_template('comment-thread.html',
                               parent_content=parent_content,
                               child_data_and_like_sum_list=zip(child_data_list, child_like_sum_list),
                               is_passage=is_passage,
                               parent_user_name=parent_user_name,
                               parent_user_id=parent_user_id,
                               current_user_id=current_user.user_id,
                               parent_post_id=parent_post_id,
                               parent_like_sum=parent_like_sum
                               )
        
    passage_data = db.session.query(Passages,
                                    Users
                                    ).join(
                                        Users,
                                        Passages.user_id == Users.user_id
                                        ).filter(Passages.passage_id==passage_id).first()

    parent_like_sum = len(PassageLikes.query.filter(PassageLikes.passage_id==passage_id).all())
    parent_content = passage_data.Passages.passage_content
    book_title = passage_data.Passages.book_title
    is_passage = True
    parent_user_name = passage_data.Users.user_name
    parent_user_id = passage_data.Passages.user_id
    passage_id = passage_data.Passages.passage_id
    
    return render_template('comment-thread.html',
                           parent_content=parent_content,
                           child_data_and_like_sum_list=zip(child_data_list, child_like_sum_list),
                           book_title=book_title,
                           is_passage=is_passage,
                           parent_user_name=parent_user_name,
                           parent_user_id=parent_user_id,
                           current_user_id=current_user.user_id,
                           parent_post_id=parent_post_id,
                           parent_like_sum=parent_like_sum,
                           passage_id=passage_id
                           )


@app.route('/submit-comment/<int:parent_post_id>', methods=['POST'])
def post_comment(parent_post_id):
    comment_content = request.form['comment_content']
    
    insert_comment_data = Comments(
        user_id=current_user.user_id,
        comment_content=comment_content,
        created_at=datetime.datetime.now()
    )
    
    db.session.add(insert_comment_data)
    db.session.commit()
    
    insert_post_ID_data = PostIDs(comment_id=insert_comment_data.comment_id)
    
    db.session.add(insert_post_ID_data)
    db.session.commit()
    
    insert_comment_relation_data = PassageCommentRelations(
        parent_id=parent_post_id,
        child_id=insert_post_ID_data.post_id
    )
    
    db.session.add(insert_comment_relation_data)
    db.session.commit()
    
    return redirect(url_for(
        'show_posts',
        post_id=parent_post_id
        )
                    )


@app.route('/comment/<string:post_id>/push-like/<int:parent_post_id>', methods=['POST'])
def push_like_button_comment(post_id, parent_post_id):
    current_user_id = current_user.user_id
    comment_id = PostIDs.query.filter_by(post_id=post_id).first().comment_id

    has_user_already_push_liked = CommentLikes.query.filter_by(comment_id=comment_id, user_id=current_user_id).first()
    
    if has_user_already_push_liked is None:
        insert_data = CommentLikes(
            user_id=current_user_id,
            comment_id=comment_id,
            created_at=datetime.datetime.now()
        )

        db.session.add(insert_data)
        db.session.commit()
    else:
        delete_data = has_user_already_push_liked
        db.session.delete(delete_data)
        db.session.commit()
    
    return redirect(url_for(
        'show_posts',
        post_id=parent_post_id
        )
                    )


@app.route('/comment/<int:comment_id>/delete/<int:parent_post_id>', methods=['POST'])
@app.route('/comment/<int:comment_id>/delete')
def delete_comment(comment_id, parent_post_id=-1):
    post_id = PostIDs.query.filter_by(comment_id=comment_id).first().post_id
    
    PassageCommentRelations.query.filter_by(parent_id=post_id).delete()
    PassageCommentRelations.query.filter_by(child_id=post_id).delete()
    CommentLikes.query.filter_by(comment_id=comment_id).delete()
    
    delete_passage_data = db.session.query(Comments).filter_by(comment_id=comment_id).first()
    delete_post_IDs_data = PostIDs.query.filter_by(comment_id=comment_id).first()
    
    db.session.delete(delete_passage_data)
    db.session.delete(delete_post_IDs_data)
    db.session.commit()
    
    if parent_post_id == -1:
        return redirect(url_for('show_main_page'))
    
    return redirect(url_for(
        'show_posts',
        post_id=parent_post_id
        )
                    )