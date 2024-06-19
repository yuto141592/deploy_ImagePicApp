from flask import Blueprint, redirect, url_for
from .extensions import db
from .models import Photo
from re import M
from flask import Flask, redirect,render_template,request,g,url_for
import matplotlib.pyplot as plt
from PIL import Image
from flask_paginate import Pagination, get_page_parameter
import os
from sqlalchemy import desc
import psycopg2


main = Blueprint('main', __name__)

def get_db():
    if 'db' not in g:
        # データベースをオープンしてFlaskのグローバル変数に保存
        g.db = psycopg2.connect(
            host='dpg-cpo5coo8fa8c73bbo7hg-a',
            port="5432",
            dbname='imagepicapp',
            user='imagepicapp_user',
            password='ZeXYZxkVbbxX7TcmiyyPLMs6EC9HL2NL'
        )
        #postgres://imagepicapp_user:ZeXYZxkVbbxX7TcmiyyPLMs6EC9HL2NL@dpg-cpo5coo8fa8c73bbo7hg-a.singapore-postgres.render.com/imagepicapp
    return g.db

# @main.route('/')
# def index():

#     # データベースを開く
#     con = get_db()

#     cur = con.execute("select count(*) from sqlite_master where TYPE='table' AND name='Images'")

#     for row in cur:
#         if row[0] == 0:
#             cur.execute("CREATE TABLE Images(id INTEGER PRIMARY KEY, image_path STRING, image_keyword STRING)")

#             con.commit()
    
#     cur = con.execute("select * from Images order by id")
#     data = cur.fetchall()
#     con.close()

#     #data = Image.query.order_by(desc(Image.id)).all()
#     #data = Photo.query.all()
#     cur = con.execute("select * from Images order by id")
#     data = cur.fetchall()
#     con.close()

    
#     page = request.args.get(get_page_parameter(), type=int, default=1)
#     res = data[(page - 1)*12: page*12]
#     pagination = Pagination(page=page, total=len(data),  per_page=12, css_framework='bootstrap4')


#     return render_template('list_index.html', data = res, pagination=pagination)

@main.route('/')
def index():

    # データベースを開く
    # con = get_db()

    # cur = con.execute("select count(*) from sqlite_master where TYPE='table' AND name='Images'")

    # for row in cur:
    #     if row[0] == 0:
    #         cur.execute("CREATE TABLE Images(id INTEGER PRIMARY KEY, image_path STRING, image_keyword STRING)")

    #         con.commit()
    
    # cur = con.execute("select * from Images order by id")
    # data = cur.fetchall()
    # con.close()

    #data = Image.query.order_by(desc(Image.id)).all()
    data = Photo.query.order_by(Photo.id).all()
    # cur = con.execute("select * from Images order by id")
    # data = cur.fetchall()
    # con.close()

    
    page = request.args.get(get_page_parameter(), type=int, default=1)
    res = data[(page - 1)*12: page*12]
    pagination = Pagination(page=page, total=len(data),  per_page=12, css_framework='bootstrap4')


    return render_template('list_index.html', data = res, pagination=pagination)

@main.route('/lists')
def index_lost():

    # # データベースを開く
    # con = get_db()

    # cur = con.execute("select count(*) from sqlite_master where TYPE='table' AND name='Images'")

    # for row in cur:
    #     if row[0] == 0:
    #         cur.execute("CREATE TABLE Images(id INTEGER PRIMARY KEY, image_path STRING, image_keyword STRING)")
            
    #         con.commit()
    
    # cur = con.execute("select * from Images order by id")
    # data = cur.fetchall()
    # con.close()

    data = Photo.query.order_by(Photo.id).all()

    # cur = con.execute("select * from Images order by id")
    # data = cur.fetchall()
    # con.close()

    page = request.args.get(get_page_parameter(), type=int, default=1)
    res = data[(page - 1)*12: page*12]
    pagination = Pagination(page=page, total=len(data),  per_page=12, css_framework='bootstrap4')


    return render_template('list_index.html', data = res, pagination=pagination)

@main.route('/result', methods=["GET", "POST"])
def result_post():

    file = request.files['example']
    file.save(os.path.join('templates/kabegami', file.filename))
    name = file.filename

    # データベースを開く
    #con = get_db()
    data2 = Photo.query.order_by(Photo.id).all()

    #cur = con.execute("select MAX(id) AS max_code from Images")
    data3 = data2[-1]
    #cur2 = con.execute("select * from Images order by id")
    #data2 = cur2.fetchall()
    list = []
    for item in data2:
        list.append(item[2])
    
    list2 = []
    for item in list:
        l = item.split(',')
        list2 = list2 + l
    list3 = []
    for i in list2:
        if i not in list3:
            list3.append(i)

    new_list = sorted(list3)

    # for row in cur:
    #     if row[0] != None:
    #         new_code = row[0] + 1
    #     else:
    #         new_code = 1
    if data3 != None:
        new_code = data3.id + 1
    else:
        new_code = 1
    # cur.close()
    # sql = "INSERT INTO Images(id, image_path, image_keyword)values({},'{}','_?/keyword/?_')".format(new_code, name)
    # con.execute(sql)
    # con.commit()
    db.session.add(Photo(id=new_code, image_path=name, image_keyword='_?/keyword/?_'))
    db.session.commit()


    # cur = con.execute("select * from Images where id = {}".format(new_code))
    # data = cur.fetchall()
    # con.close()
    data = Photo.query.filter_by(id=new_code).all()
    
    return render_template('register.html', data = data, list=new_list)

@main.route("/register", methods=["POST"])
def register():
    
    #con = get_db()
    data = Photo.query.filter(Photo.image_keyword.like('%_?/keyword/?_%')).all()
    #sql3 = "select * from Images where image_keyword LIKE '%_?/keyword/?_%'"
    #cur = con.execute("select *  from Images where id = MAX(id)")
    # cur = con.execute(sql3)
    # data = cur.fetchall()
    
    
    data1 = data[0][0]
    data1_ = int(data1)
    data2 = data[0][1]
    data2_ = str(data2)
   
    new_key = request.form.get("key")

    # sql2 = "DELETE FROM Images WHERE image_keyword LIKE '%_?/keyword/?_%'"
    # con.execute(sql2)
    # con.commit()
    delImg = Photo.query.filter(Photo.image_keyword.like('%_?/keyword/?_%')).first()
    db.session.delete(delImg)
    db.session.commit()
   
    # sql4 = "insert into Images(id, image_path, image_keyword) values({}, '{}', '{}')".format(data1_, data2_, new_key)
    # con.execute(sql4)
    # con.commit()
    # cur = con.execute("select * from Images order by id")
    # data = cur.fetchall()

    db.session.add(Photo(id=data1_, image_path=data2_, image_keyword=new_key))
    db.session.commit()
    data = Photo.query.order_by(Photo.id).all()
    
    #con.close()

    page = request.args.get(get_page_parameter(), type=int, default=1)
    res = data[(page - 1)*12: page*12]
    pagination = Pagination(page=page, total=len(data),  per_page=12, css_framework='bootstrap4')


    render_template('list_index.html', data = res, pagination=pagination)
    return redirect("/lists")



@main.route("/delete/<int:id>", methods=["GET"])
def delete_post(id):

    # con = get_db()

    # sql2 = "DELETE FROM Images WHERE id = {}".format(id)
    # con.execute(sql2)
    # con.commit()

    # cur = con.execute("select * from Images order by id")
    # data = cur.fetchall()
    # con.close()

    delImg = Photo.query.get(id)
    db.session.delete(delImg)
    db.session.commit()

    data = Photo.query.order_by(Photo.id).all()

    page = request.args.get(get_page_parameter(), type=int, default=1)
    res = data[(page - 1)*12: page*12]
    pagination = Pagination(page=page, total=len(data),  per_page=12, css_framework='bootstrap4')

    render_template('list_index.html', data = res, pagination=pagination)
    return redirect("/lists")

@main.route("/open_image/<int:id>")
def open_image(id):
    # con = get_db()
    # sql = "select image_path from Images where id={}".format(id)
    # cur = con.execute(sql)
    # image = cur.fetchall()
    # con.close()

    #image = Photo.query.with_entities(Photo.image_path).get(id)
    img_id = id 
    image = Photo.query.filter_by(id=img_id).with_entities(Photo.image_path).scalar()

    image2 = str(image)
    
    # PIL.Imageで画像を開く
    pic = image2.strip("[")
    pic2 = pic.strip("]")
    pic3 = pic2.strip("(")
    pic4 = pic3.strip(")")
    pic5 = pic4.strip(",")
    pic6 = pic5.strip("'")
    
    path = "templates/kabegami/{}".format(pic6)
    
    img = Image.open(path)
    # OS標準の画像ビューアで表示
    img.show()
    
    return redirect("/")

@main.route("/row_image", methods=["POST"])
def row_image():
    im = request.form["check"]
    # con = get_db()
    # cur = con.execute("select * from Images where image_keyword LIKE '%{}%'".format(im))
    # data = cur.fetchall() 
    
    #con.close()
    data = data = Photo.query.filter(Photo.image_keyword.like('%{}%'.format(im))).all()

    return render_template("images.html", data=data)

@main.route("/result2")
def open_image2():
    # con = get_db()

    # cur = con.execute("select * from Images order by id")
    # data = cur.fetchall()
    # con.close()

    data = Photo.query.order_by(Photo.id).all()

    list = []
    for item in data:
        list.append(item[2])
    
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
def list_open():
    # con = get_db()
    # cur = con.execute("select * from Images order by id")
    # data = cur.fetchall()
    # con.close()

    data = Photo.query.order_by(Photo.id).all()

    page = request.args.get(get_page_parameter(), type=int, default=1)
    res = data[(page - 1)*12: page*12]
    pagination = Pagination(page=page, total=len(data),  per_page=12, css_framework='bootstrap4')

    return render_template('list_index.html', data = res, pagination=pagination)

@main.route("/update/<int:id>")
def update(id):
    # con = get_db()
    # sql3 = "select * from Images where id = {}".format(id)
    
    # cur = con.execute(sql3)
    # data = cur.fetchall()
    # con.close()

    data = Photo.query.get(id)
    
    return render_template('update.html', data = data)
    
    
@main.route("/update/<int:id>", methods=["POST"])
def update_post(id):
    # con = get_db()
    # sql3 = "select * from Images where id = {}".format(id)
    # cur = con.execute(sql3)
    # data = cur.fetchall()
    
    data = Photo.query.get(id)
    
    data1 = data[0][0]
    data1_ = int(data1)
    data2 = data[0][1]
    data2_ = str(data2)
   
    new_key = request.form.get("key_word")

    # sql2 = "DELETE FROM Images WHERE id = {}".format(id)
    # con.execute(sql2)
    # con.commit()
    db.session.delete(data)
    db.session.commit()

   
    # sql4 = "insert into Images(id, image_path, image_keyword) values({}, '{}', '{}')".format(data1_, data2_, new_key)
    # con.execute(sql4)
    # con.commit()
    # cur = con.execute("select * from Images order by id")
    # data = cur.fetchall()
    
    # con.close()
    new_img = Photo(id=data1_, image_path=data2_, image_keyword=new_key)
    db.session.add(new_img)
    db.session.commit()

    
    return redirect("/list")

@main.route("/about_index")
def about():
    return render_template('about_index.html')
