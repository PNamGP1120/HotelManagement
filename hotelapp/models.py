from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float, Enum
from sqlalchemy.orm import relationship
from hotelapp import db, app
from enum import Enum as RoleEnum
from flask_login import UserMixin

class UserRole(RoleEnum):
    ADMIN = 1
    USER = 2

class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    avatar = Column(String(100),
                    default='https://res.cloudinary.com/dxxwcby8l/image/upload/v1679134375/ckvdo90ltnfns77zf1xb.jpg')
    user_role = Column(Enum(UserRole), default=UserRole.USER)
    CCCD = Column(String(15), nullable=False)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        import hashlib
        u = User(username='admin',
                 name = 'admin',
                 password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
                 user_role=UserRole.ADMIN, CCCD = '072')
        u2 = User(name='Dang Phuong Nam',
                  username='phnam',
                 password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
                 user_role=UserRole.USER, CCCD='072204')
        db.session.add(u)
        db.session.add(u2)
        db.session.commit()
