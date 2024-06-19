
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
from config import Config
import psycopg2



def create_app():
    app = Flask(__name__, static_folder="./templates/kabegami")
    app.config.from_object(Config)


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
