from sqlalchemy.sql import func
from web import db

class Enquiry(db.Model):
    __tablename__ = 'enquiries'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=True)
    phone = db.Column(db.String(15), nullable=True)
    title = db.Column(db.Integer, nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __init__(self, first_name=None, last_name=None, title=None, message=None):
        self.title = title
        self.first_name = first_name
        self.last_name = last_name
        self.message = message

    def __repr__(self):
        return f'<Enquiry {self.title!r}>'

