
from re import M
from flask import Flask, redirect,render_template,request,g,url_for
import matplotlib.pyplot as plt
from PIL import Image
from flask_paginate import Pagination, get_page_parameter
from flask import Flask
from .extensions import db
from .routes import main
from .models import User
from config import Config
from firebase_admin import credentials, initialize_app
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from firebase_admin import credentials
import flask_devices

def create_app():
   
    app = Flask(__name__, static_folder="./templates/kabegami")
    app.config.from_object(Config)

    devices = flask_devices.Devices(app)
    devices.add_pattern('mobile', 'iPhone|iPod|Android.*Mobile|Windows.*Phone|dream|blackberry|CUPCAKE|webOS|incognito|webmate', 'app/templates/mobile')
    devices.add_pattern('tablet', 'iPad|Android', 'app/templates')
    devices.add_pattern('pc', '.*', 'app/templates')

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

    return app
