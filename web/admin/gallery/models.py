from sqlalchemy.sql import func
from web import db

class Photobook(db.Model):
    __tablename__ = 'photobooks'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    images = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())


    def __init__(self, user=None, title=None, description=None, images=None):
        self.title = title
        self.user = user
        self.description = description
        self.images = images

    def __repr__(self):
        return f'<Photobook {self.title!r}>'

