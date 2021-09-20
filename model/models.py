# coding: UTF-8
import base64

from flask_login import UserMixin

import config
DB = config.DB

with open('static/img/sample_image_human.png', mode='rb') as f:
    default_user_image_base64 = base64.b64encode(f.read())


class Passages(DB.Model):
    
    __tablename__ = 'passages'
    
    passage_id = DB.Column(DB.Integer, primary_key=True)
    user_id = DB.Column(DB.String(128), DB.ForeignKey('users.user_id'), nullable=False)
    book_title = DB.Column(DB.String(128), nullable=False, default='不明')
    post_content = DB.Column(DB.String(128), nullable=False)
    created_at = DB.Column(DB.DateTime, nullable=False)


class PassageRelations(DB.Model):
    
    __tablename__ = 'passage_relations'
    
    passage_relation_id = DB.Column(DB.Integer, primary_key=True)
    parent_passage_id = DB.Column(DB.Integer, DB.ForeignKey('passages.passage_id'), nullable=False)
    child_passage_id = DB.Column(DB.Integer, DB.ForeignKey('passages.passage_id'), nullable=False)


# flaskではint型のidを元にユーザーログイン情報管理を行なっており、user_idはvarchar型なのでidとuser_idを持ったテーブルを作ることでログイン情報を管理している
class UserLoginInformation(UserMixin, DB.Model):
    
    __tablename__ = 'user_login_informations'
    
    id = DB.Column(DB.Integer, primary_key=True)
    user_id = DB.Column(DB.String(128), DB.ForeignKey('users.user_id'), nullable=False)


class Users(DB.Model):
    
    __tablename__ = 'users'
    
    user_id = DB.Column(DB.String(128), nullable=False, primary_key=True)
    password = DB.Column(DB.String(128), nullable=False)
    user_name = DB.Column(DB.String(128), nullable=False)
    email_address = DB.Column(DB.String(128), nullable=False)
    self_introduction = DB.Column(DB.String(128), nullable=False, default='')
    user_image = DB.Column(DB.LargeBinary, nullable=False, default=default_user_image_base64)


class PassageLikes(DB.Model):
    
    __tablename__ = 'passage_likes'
    
    like_id = DB.Column(DB.Integer, primary_key=True)
    user_id = DB.Column(DB.String(128), DB.ForeignKey('users.user_id'), nullable=False)
    passage_id = DB.Column(DB.Integer, DB.ForeignKey('passages.passage_id'), nullable=False)