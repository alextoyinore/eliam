from sqlalchemy.sql import func
from web import db

class Hymn(db.Model):
    __tablename__ = 'hymns'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    def __init__(self, title=None, user=None, content=None):
        self.title = title
        self.user = user
        self.content = content

    def __repr__(self):
        return f'<Hymn {self.title!r}>'

