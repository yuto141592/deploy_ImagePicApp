from flask import Blueprint, redirect, url_for, Flask, jsonify, render_template, flash, render_template_string, request,g, session
from .extensions import db
from .models import User, Images
from PIL import Image
from flask_paginate import Pagination, get_page_parameter
import os
from sqlalchemy import desc
import psycopg2
from werkzeug.utils import secure_filename
import pyrebase
import firebase_admin
from firebase_admin import credentials, auth as admin_auth, storage
from firebase import firebase
import json
from datetime import timedelta
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required



main = Blueprint('main', __name__)

firebase_sdk_str = os.getenv('FIRE_BASE_SDK')
firebase_sdk = json.loads(firebase_sdk_str)
firebase = pyrebase.initialize_app(firebase_sdk)


firebase_config_str = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
firebase_config = json.loads(firebase_config_str)
cred = credentials.Certificate(firebase_config)
firebase_admin.initialize_app(cred, {
    'storageBucket': 'imagepicapp.appspot.com'
})

aut = firebase.auth()


@main.route('/', methods=['GET', 'POST'])
def login_f():
    if request.method == 'POST':
        
        email = request.form['email']
        password = request.form['password']
 
        user = User.query.filter_by(email=email).first()
        if user is not None:

            if user.check_password(password):

                try:
                    user2 = aut.sign_in_with_email_and_password(email, password)

                    id_token = user2['idToken']

                    decoded_token = admin_auth.verify_id_token(id_token)
                    uid = decoded_token['uid']
                    session['user'] = uid

                    login_user(user)
                    next = request.args.get('next')
                    if next == None or not next[0] == '/':
                        next = url_for('main.index_lost')
                    return redirect(next)
                    
                except Exception as e:
                    flash('Login failed. Please check your credentials', 'danger')
                    print(e)
                
            else:
                flash('パスワードが一致しません')
        else:
            flash('入力されたユーザーは存在しません')

    return render_template('login.html')


@main.route('/lists')
@login_required
def index_lost():


    data = Images.query.filter(Images.user_id==session['user']).order_by(Images.id).all()

    new_data = []
    for d in data:
        d_path = d.image_path
        bucket = storage.bucket()
        blob = bucket.blob(d_path)
        file_url = blob.generate_signed_url(timedelta(minutes=15))
        new_l = [file_url, d.image_name, d.image_keyword, d.id]
        new_data.append(new_l)

    page = request.args.get(get_page_parameter(), type=int, default=1)
    res = new_data[(page - 1)*12: page*12]
    pagination = Pagination(page=page, total=len(data),  per_page=12, css_framework='bootstrap4')
    

    return render_template('list_index.html', data = res, pagination=pagination)

@main.route('/result', methods=["GET", "POST"])
@login_required
def result_post():
    if 'user' not in session:
        return redirect(url_for('main.login'))
     
    file = request.files['example']
    if file:
        file_path = 'app/templates/kabegami' + '/' + file.filename

        file.save(file_path)
        name = f"{session['user']}/{file.filename}"

 
        data2 = Images.query.filter(Images.user_id==session['user']).order_by(Images.id).all()
        data3 = Images.query.order_by(Images.id.desc()).first()

        list = []
        for item in data2:
            list.append(item.image_keyword)
        
        list2 = []
        for item in list:
            l = item.split(',')
            list2 = list2 + l
        list3 = []
        for i in list2:
            if i not in list3:
                list3.append(i)

        new_list = sorted(list3)

        if data3 != None:
            new_code = data3.id + 1
        else:
            new_code = 1

        db.session.add(Images(id=new_code, user_id=session['user'], image_path=name, image_keyword='_?/keyword/?_'))
        db.session.commit()    

        bucket = storage.bucket()
        blob = bucket.blob(f"{session['user']}/{file.filename}")
        blob.upload_from_filename(file_path)

        os.remove(file_path)

        data = Images.query.filter(Images.id==new_code, Images.user_id==session['user']).first()

        new_data = data

        d_path = new_data.image_path
        bucket = storage.bucket()
        blob = bucket.blob(d_path)
        file_url = blob.generate_signed_url(timedelta(minutes=15))
        new_l = [file_url, new_data.id]
        
        return render_template('register.html', data = new_l, list=new_list)

@main.route("/register", methods=["POST"])
@login_required
def register():
    

    data = Images.query.filter(Images.user_id==session['user']).filter(Images.image_keyword.like('%_?/keyword/?_%')).all()
 
    data1 = data[0].id
    data1_ = int(data1)
    data2 = data[0].image_path
    data2_ = str(data2)
   
    get_item = request.form.getlist("item")
    new_name = str(get_item[0])
    new_key = str(get_item[1])

    delImg = Images.query.filter(Images.user_id==session['user']).filter(Images.image_keyword.like('%_?/keyword/?_%')).first()
    db.session.delete(delImg)
    db.session.commit()


    db.session.add(Images(id=data1_, user_id=session['user'], image_name=new_name, image_path=data2_, image_keyword=new_key))
    db.session.commit()
    data = Images.query.filter(Images.user_id==session['user']).order_by(Images.id).all()
    
    new_data = []
    for d in data:
        d_path = d.image_path
        bucket = storage.bucket()
        blob = bucket.blob(d_path)
        file_url = blob.generate_signed_url(timedelta(minutes=15))
        new_l = [file_url, d.image_name, d.image_keyword, d.id]
        new_data.append(new_l)

    page = request.args.get(get_page_parameter(), type=int, default=1)
    res = new_data[(page - 1)*12: page*12]
    pagination = Pagination(page=page, total=len(new_data),  per_page=12, css_framework='bootstrap4')


    render_template('list_index.html', data = res, pagination=pagination)
    return redirect("/lists")



@main.route("/delete/<int:id>", methods=["GET"])
@login_required
def delete_post(id):


    file_path = Images.query.filter(Images.user_id==session['user']).filter(Images.id==id).first()
    delPath = file_path.image_path
    bucket = storage.bucket()
    blob = bucket.blob(delPath)
    blob.delete()

    delImg = Images.query.filter_by(user_id=session['user'], id=id).first()
    db.session.delete(delImg)
    db.session.commit()


    data = Images.query.filter(Images.user_id==session['user']).order_by(Images.id).all()
    new_data = []
    for d in data:
        d_path = d.image_path
        bucket = storage.bucket()
        blob = bucket.blob(d_path)
        file_url = blob.generate_signed_url(timedelta(minutes=15))
        new_l = [file_url, d.image_name, d.image_keyword, d.id]
        new_data.append(new_l)

    page = request.args.get(get_page_parameter(), type=int, default=1)
    res = new_data[(page - 1)*12: page*12]
    pagination = Pagination(page=page, total=len(new_data),  per_page=12, css_framework='bootstrap4')

    render_template('list_index.html', data = res, pagination=pagination)
    return redirect("/lists")

@main.route("/open_image/<int:id>")
@login_required
def open_image(id):

    img_id = id 
    image = Images.query.filter(Images.id==img_id, user_id=session['user']).with_entities(Images.image_path).scalar()

    image2 = str(image)
    
    # PIL.Imageで画像を開く
    pic = image2.strip("[")
    pic2 = pic.strip("]")
    pic3 = pic2.strip("(")
    pic4 = pic3.strip(")")
    pic5 = pic4.strip(",")
    pic6 = pic5.strip("'")
    
    path = "app/templates/kabegami/{}".format(pic6)
    
    img = Image.open(path)
    # OS標準の画像ビューアで表示
    img.show()
    
    return redirect("/lists")

@main.route("/row_image", methods=["POST"])
@login_required
def row_image():
    im = request.form["check"]

    data = Images.query.filter(Images.user_id==session['user']).filter(Images.image_keyword.like('%{}%'.format(im))).all()

    return render_template("images.html", data=data)

@main.route("/result2")
@login_required
def open_image2():

    data = Images.query.filter(Images.user_id==session['user']).order_by(Images.id).all()

    list = []
    for item in data:
        list.append(item.image_keyword)
    
    list2 = []
    for item in list:
        l = item.split(',')
        list2 = list2 + l
    list3 = []
    for i in list2:
        if i not in list3:
            list3.append(i)

    new_list = sorted(list3)
    
    return render_template('index_image.html', data=data, list=new_list)

    
@main.route("/list")
@login_required
def list_open():


    data = Images.query.filter(Images.user_id==session['user']).order_by(Images.id).all()

    page = request.args.get(get_page_parameter(), type=int, default=1)
    res = data[(page - 1)*12: page*12]
    pagination = Pagination(page=page, total=len(data),  per_page=12, css_framework='bootstrap4')

    return render_template('list_index.html', data = res, pagination=pagination)

@main.route("/update/<int:id>")
@login_required
def update(id):
    data = Images.query.filter(Images.user_id==session['user']).get(id)
    
    return render_template('update.html', data = data)
    
    
@main.route("/update/<int:id>", methods=["POST"])
@login_required
def update_post(id):

    data = Images.query.filter(Images.user_id==session['user']).get(id)
    
    data1 = data[0].id
    data1_ = int(data1)
    data2 = data[0].image_path
    data2_ = str(data2)
   
    new_key = request.form.get("key_word")

    db.session.delete(data)
    db.session.commit()

    new_img = Images(id=data1_, user_id=session['user'], image_path=data2_, image_keyword=new_key)
    db.session.add(new_img)
    db.session.commit()

    
    return redirect("/list")

@main.route("/about_index")
def about():
    return render_template('about_index.html')

@main.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user is None:
            user = User(email=email, password_hash=password)
            db.session.add(user)
            db.session.commit()
            try:
                user = admin_auth.create_user(email=email, email_verified=False, password=password, display_name='John Doe', disabled=False)
                flash('Account created successfully', 'success')
                return redirect(url_for('main.login'))
            except Exception as e:
                flash('Account creation failed. Please try again.', 'danger')
                print(e)
            
        else:
            flash('すでにサインアップされています')
    

    return render_template('signup.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        
        email = request.form['email']
        password = request.form['password']
 
        user = User.query.filter_by(email=email).first()
        if user is not None:

            if user.check_password(password):

                try:
                    user2 = aut.sign_in_with_email_and_password(email, password)

                    id_token = user2['idToken']

                    decoded_token = admin_auth.verify_id_token(id_token)
                    uid = decoded_token['uid']
                    session['user'] = uid

                    login_user(user)
                    next = request.args.get('next')
                    if next == None or not next[0] == '/':
                        next = url_for('main.index_lost')
                    return redirect(next)
                    
                except Exception as e:
                    flash('Login failed. Please check your credentials', 'danger')
                    print(e)
                
            else:
                flash('パスワードが一致しません')
        else:
            flash('入力されたユーザーは存在しません')

    return render_template('login.html')


@main.route('/logout')
@login_required
def logout():
    session.pop('user', None)
    logout_user()
    return redirect(url_for('main.login'))

@main.route('/upload')
@login_required
def upload_form():
    if 'user' not in session:
        return redirect(url_for('main.index_lost'))
    return '''
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <title>Upload Image</title>
      </head>
      <body>
        <h1>Upload Image</h1>
        <form method="POST" enctype="multipart/form-data" action="/upload_file">
          <input type="file" name="file">
          <input type="submit" value="Upload">
        </form>
      </body>
    </html>
    '''

@main.route('/upload_file', methods=['POST'])
@login_required
def upload_file():
    if 'user' not in session:
        return redirect(url_for('main.login'))
    
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            file_path = 'app/templates/kabegami' + '/' + file.filename
            file.save(file_path)
            
            # Firebase Storageにファイルをアップロード
            bucket = storage.bucket()
            blob = bucket.blob(f"{session['user']}/{filename}")
            blob.upload_from_filename(file_path)
            
            # ファイルを削除
            os.remove(file_path)

            # blob.make_public()  # ファイルを公開
            file_url = blob.generate_signed_url(timedelta(minutes=15))  # URLの有効期限を15分に設定
            
            flash('File successfully uploaded', 'success')
            return redirect(url_for('main.dashboard', file_url=file_url))
    
@main.route('/dashboard')
@login_required
def dashboard():
    file_url = request.args.get('file_url')
    return render_template('dashboard.html', file_url=file_url)
    
   
