from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote
from flask_login import LoginManager
import cloudinary

app = Flask(__name__)
app.secret_key = 'HJGFGHF^&%^&&*^&*YUGHJGHJF^%&YYHB'
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:%s@localhost/hotel?charset=utf8mb4" % quote('Admin@123')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["PAGE_SIZE"] = 6
app.config['SESSION_TYPE'] = 'filesystem'

db = SQLAlchemy(app)
login = LoginManager(app)

cloudinary.config(
    cloud_name = 'dqpu49bbo',
    api_key = '743773348627895',
    api_secret = 'EF7elKsibuI8JEBqfMNZYYWUYvo',
    secure = True
)