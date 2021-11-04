from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_folder='static')
app.config.from_object('bukuemo.config')
db = SQLAlchemy(app)

import bukuemo.models

db.create_all()

import bukuemo.views