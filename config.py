import os

class Config:

    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    #SECRET_KEY = '8e9066bc94cf595ec3fdb445190128e6'
    FIREBASE_CONFIG = os.getenv('FIRE_BASE_SDK')
    #FIREBASE_CONFIG = "fireBaseSDK.json"

