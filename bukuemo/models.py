# coding: UTF-8
import base64

from flask_login import UserMixin

from bukuemo import db

with open('bukuemo/static/img/sample_image_human.png', mode='rb') as f:
    default_user_image_base64 = base64.b64encode(f.read())


class Comments(db.Model):
    
    __tablename__ = 'comments'
    
    comment_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(128), db.ForeignKey('users.user_id'), nullable=False)
    comment_content = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)


class CommentLikes(db.Model):
    
    __tablename__ = 'comment_likes'
    
    like_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(128), db.ForeignKey('users.user_id'), nullable=False)
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.comment_id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)


class Passages(db.Model):
    
    __tablename__ = 'passages'
    
    passage_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(128), db.ForeignKey('users.user_id'), nullable=False)
    book_title = db.Column(db.String(128), nullable=False, default='不明')
    passage_content = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)


class PostCommentRelations(db.Model):
    
    __tablename__ = 'post_comment_relations'
    
    post_comment_relation_id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('post_IDs.post_id'), nullable=False)
    child_id = db.Column(db.Integer, db.ForeignKey('post_IDs.post_id'), nullable=False, default=-1)  # -1の時はchild_idとなるべきものがない場合


class PassageLikes(db.Model):
    
    __tablename__ = 'passage_likes'
    
    like_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(128), db.ForeignKey('users.user_id'), nullable=False)
    passage_id = db.Column(db.Integer, db.ForeignKey('passages.passage_id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)


# /posts/post_idのURLで紐づいたリプライがなくても表示したい投稿はあるので投稿をinsertする際にこのテーブルにも追加する
class PostIDs(db.Model):
    
    __tablename__ = 'post_IDs'
    
    post_id = db.Column(db.Integer, primary_key=True)
    passage_id = db.Column(db.Integer, db.ForeignKey('passages.passage_id'), nullable=False, default=-1)
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.comment_id'), nullable=False, default=-1)


# flaskではint型のidを元にユーザーログイン情報管理を行なっており、user_idはvarchar型なのでidとuser_idを持ったテーブルを作ることでログイン情報を管理している
class UserLoginInformation(UserMixin, db.Model):
    
    __tablename__ = 'user_login_informations'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(128), db.ForeignKey('users.user_id'), nullable=False)
    
    def get_id(self):
        return self.user_id


class Users(db.Model):
    
    __tablename__ = 'users'
    
    user_id = db.Column(db.String(128), nullable=False, primary_key=True)
    password = db.Column(db.String(128), nullable=False)
    user_name = db.Column(db.String(128), nullable=False)
    email_address = db.Column(db.LargeBinary, nullable=False)
    self_introduction = db.Column(db.String(128), nullable=False, default='')
    user_image = db.Column(db.LargeBinary, nullable=False, default=default_user_image_base64)
    created_at = db.Column(db.DateTime, nullable=False)

def init():
    db.create_all()