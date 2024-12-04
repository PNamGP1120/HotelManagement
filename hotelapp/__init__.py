from flask import Flask
from urllib.parse import quote
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import cloudinary

app = Flask(__name__)
app.secret_key = "KJGHJG^&*%&IGFG%ERFTGHCFHGF^&**&TYIU"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://pnam:%s@localhost/hotel?charset=utf8mb4" % quote('Phuongnam0212@')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
# app.config["PAGE_SIZE"] = 8

db = SQLAlchemy(app)
# login = LoginManager(app)
#
# cloudinary.config(
#     cloud_name = 'dqpu49bbo',
#     api_key = '743773348627895',
#     api_secret = 'EF7elKsibuI8JEBqfMNZYYWUYvo',
# )