from sqlalchemy.sql import func
from web import db

class Member(db.Model):
    __tablename__ = 'members'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user = db.Column(db.Integer, nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    middle_name = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(100), nullable=True, unique=True)
    date_of_birth = db.Column(db.Date, nullable=True)
    occupation = db.Column(db.String(200), nullable=True)
    house_no = db.Column(db.Integer, nullable=True)
    street = db.Column(db.String(100), nullable=True)
    city = db.Column(db.String(100), nullable=True)
    state = db.Column(db.String(100), nullable=True)
    country = db.Column(db.String(100), nullable=True)
    department = db.Column(db.String(100), nullable=True)
    date_joined = db.Column(db.Date, nullable=True)
    year_baptized = db.Column(db.Date, nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())


    def __init__(self, first_name=None, last_name=None, user=None):
        self.user = user
        self.first_name = first_name
        self.last_name = last_name

    def __repr__(self):
        return f'<Member {self.first_name!r} {self.last_name!r}>'

