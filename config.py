import os

class Config:
    #SQLALCHEMY_DATABASE_URI = os.getenv('postgresql://imagepicapp_user:ZeXYZxkVbbxX7TcmiyyPLMs6EC9HL2NL@dpg-cpo5coo8fa8c73bbo7hg-a.singapore-postgres.render.com/imagepicapp')
    SQLALCHEMY_DATABASE_URI = 'postgresql://imagepicapp_user:ZeXYZxkVbbxX7TcmiyyPLMs6EC9HL2NL@dpg-cpo5coo8fa8c73bbo7hg-a.singapore-postgres.render.com/imagepicapp'
    #SQLALCHEMY_DATABASE_URI = 'postgresql://imagepicapp_user:ZeXYZxkVbbxX7TcmiyyPLMs6EC9HL2NL@dpg-cpo5coo8fa8c73bbo7hg-a/imagepicapp'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    #SECRET_KEY = os.getenv('8e9066bc94cf595ec3fdb445190128e6')
    SECRET_KEY = '8e9066bc94cf595ec3fdb445190128e6'
