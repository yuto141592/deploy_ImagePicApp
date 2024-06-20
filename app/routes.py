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


# @main.route('/upload_file', methods=['POST'])
# @login_required
# def upload_file():
#     if 'user' not in session:
#         return redirect(url_for('main.login'))
    
#     if request.method == 'POST':
#         file = request.files['file']
#         if file:
#             filename = secure_filename(file.filename)
#             file_path = 'app/templates/kabegami' + '/' + file.filename
#             file.save(file_path)
            
#             # Firebase Storageにファイルをアップロード
#             bucket = storage.bucket()
#             blob = bucket.blob(f"{session['user']}/{filename}")
#             blob.upload_from_filename(file_path)
            
#             # ファイルを削除
#             os.remove(file_path)

#             # blob.make_public()  # ファイルを公開
#             file_url = blob.generate_signed_url(timedelta(minutes=15))  # URLの有効期限を15分に設定
            
#             flash('File successfully uploaded', 'success')
#             return redirect(url_for('main.dashboard', file_url=file_url))
