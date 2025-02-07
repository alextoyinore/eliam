from sqlalchemy.sql import func
from web import db

class Training(db.Model):
    __tablename__ = 'trainings'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    def __init__(self, user=None, title=None, start_date=None, end_date=None, description=None):
        self.user = user
        self.title = title
        self.start_date = start_date
        self.end_date = end_date
        self.description = description

    def __repr__(self):
        return f'<Training {self.title!r} {self.start_date!r} {self.end_date!r}>'

