from sqlalchemy.sql import func
from web import db

class Testimony(db.Model):
    __tablename__ = 'testimonies'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user = db.Column(db.Integer, nullable=True)
    member = db.Column(db.Integer, nullable=True)
    first_name = db.Column(db.String(100), nullable=True)
    last_name = db.Column(db.String(100), nullable=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    def __init__(self, user=None, member=None, first_name=None, last_name=None, title=None, content=None):
        self.user = user
        self.member = member
        self.first_name = first_name
        self.last_name = last_name
        self.title = title
        self.content = content

    def __repr__(self):
        return f'<Testimony {self.content!r}>'

