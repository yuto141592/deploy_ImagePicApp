from .extensions import db

class Photo(db.Model):
    __tablename__ = 'Images'
    id = db.Column(db.Integer, primary_key=True)
    image_path = db.Column(db.String(50))
    image_keyword = db.Column(db.String(50))
