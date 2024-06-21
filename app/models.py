from .extensions import db
from flask_login import UserMixin
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash


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


