from sqlalchemy.sql import func
from web import db

class Prayer(db.Model):
    __tablename__ = 'prayer_requests'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    is_member = db.Column(db.Boolean, default=False, nullable=True)
    first_name = db.Column(db.String(100), nullable=True)
    last_name = db.Column(db.String(100), nullable=True)
    title = db.Column(db.String(100), nullable=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    def __init__(self, is_member=None, first_name=None, last_name=None, title=None, content=None):
        self.first_name = first_name
        self.last_name = last_name
        self.is_member = is_member
        self.title = title
        self.content = content

    def __repr__(self):
        return f'<Notice {self.content!r}>'

