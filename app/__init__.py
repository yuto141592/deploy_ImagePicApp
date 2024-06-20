
from re import M
import sqlite3
from flask import Flask, redirect,render_template,request,g,url_for
import matplotlib.pyplot as plt
from PIL import Image
from flask_paginate import Pagination, get_page_parameter
import os
from flask import Flask
from .extensions import db
from .routes import main
from .models import User
from config import Config
import psycopg2
from firebase_admin import credentials, initialize_app
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
import firebase_admin
from firebase_admin import credentials

def create_app():
   
    app = Flask(__name__, static_folder="./templates/kabegami")
    app.config.from_object(Config)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'


    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    def localize_callback(*args, **kwarg):
        return 'このページにアクセスするには、ログインが必要です'
    login_manager.localize_callback = localize_callback


    db.init_app(app)
    app.register_blueprint(main)

    with app.app_context():
        try:
            db.create_all()
            print("PostgreSQL に接続成功しました！")
        except Exception as e:
            print(f"PostgreSQL への接続中にエラーが発生しました: {e}")
    # with app.app_context():
    #     from .routes import main
    #     app.register_blueprint(main)
    #     try:
    #         conn = psycopg2.connect(
    #             host='dpg-cpo5coo8fa8c73bbo7hg-a',
    #             port="5432",
    #             dbname='imagepicapp',
    #             user='imagepicapp_user',
    #             password='ZeXYZxkVbbxX7TcmiyyPLMs6EC9HL2NL'
    #         )
    #         print("Connection successful")
    #         conn.close()
    #     except psycopg2.OperationalError as e:
    #         print(f"Connection failed: {e}")


    return app
