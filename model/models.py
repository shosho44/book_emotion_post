# coding: UTF-8
import base64

from flask_login import UserMixin

from ..config import db


with open('static/img/sample_image_human.png', mode='rb') as f:
    default_user_image_base64 = base64.b64encode(f.read())


class Passages(db.Model):
    
    __tablename__ = 'passages'
    
    passage_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(128), db.ForeignKey('users.user_id'), nullable=False)
    book_title = db.Column(db.String(128), nullable=False, default='不明')
    post_content = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    good_sum = db.Column(db.Integer, nullable=False, default=0)


class PassageRelations(db.Model):
    
    __tablename__ = 'passage_relations'
    
    passage_relation_id = db.Column(db.Integer, primary_key=True)
    parent_passage_id = db.Column(db.Integer, db.ForeignKey('passages.passage_id'), nullable=False)
    child_passage_id = db.Column(db.Integer, db.ForeignKey('passages.passage_id'), nullable=False)


# flaskではint型のidを元にユーザーログイン情報管理を行なっており、user_idはvarchar型なのでidとuser_idを持ったテーブルを作ることでログイン情報を管理している
class UserLoginInformation(UserMixin, db.Model):
    
    __tablename__ = 'user_login_informations'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(128), db.ForeignKey('users.user_id'), nullable=False)


class Users(db.Model):
    
    __tablename__ = 'users'
    
    user_id = db.Column(db.String(128), nullable=False, primary_key=True)
    password = db.Column(db.String(128), nullable=False)
    user_name = db.Column(db.String(128), nullable=False)
    email_address = db.Column(db.String(128), nullable=False)
    self_introduction = db.Column(db.String(128), nullable=False, default='')
    user_image = db.Column(db.LargeBinary, nullable=False, default=default_user_image_base64)


class PassageLikes(db.Model):
    
    __tablename__ = 'passage_likes'
    
    like_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(128), db.ForeignKey('users.user_id'), nullable=False)
    passage_id = db.Column(db.Integer, db.ForeignKey('passages.passage_id'), nullable=False)