from .extensions import db
from flask_login import UserMixin
import firebase_admin
from firebase_admin import auth
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash



class Photo(db.Model):
    __tablename__ = 'Images'
    id = db.Column(db.Integer, primary_key=True)
    # user_id = db.Column(db.String(64), unique=True, index=True)
    image_path = db.Column(db.String(50))
    image_keyword = db.Column(db.String(50))

class Photo2(db.Model):
    __tablename__ = 'Images2'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(64), unique=False)
    image_path = db.Column(db.String(50))
    image_keyword = db.Column(db.String(50))

class Photo3(db.Model):
    __tablename__ = 'Images3'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(64))
    image_path = db.Column(db.String(50))
    image_keyword = db.Column(db.String(50))

class Images(db.Model):
    __tablename__ = 'ImgDB'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(64))
    image_name = db.Column(db.String(64))
    image_path = db.Column(db.String(64))
    image_keyword = db.Column(db.String(64))

#UserMixinをを継承
class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(64), unique=True, index=True)
    # username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    def check_password(self, password):
        if self.password_hash == password:
            return True
        return False


