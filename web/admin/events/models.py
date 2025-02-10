from sqlalchemy.sql import func
from web import db
from web.admin.users.models import User

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user = db.Column(db.Integer, nullable=False)
    title = db.Column(db.Integer, nullable=False)
    start_date = db.Column(db.DateTime(timezone=True), nullable=False)
    end_date = db.Column(db.DateTime(timezone=True), nullable=False)
    start_time = db.Column(db.Time, unique=True, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    event_type = db.Column(db.String(50), nullable=True)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    is_published = db.Column(db.Boolean, default=False, nullable=False)


    @property
    def get_user(self):
        return User.query.get(pk=self.user)

    @property
    def event_date(self):
        return f'{self.start_date} - {self.end_date}'

    @property
    def event_time(self):
        return f'{self.start_time} - {self.end_time}'

    def __init__(self, title=None, start_date=None, 
                 end_date=None, start_time=None, user=None,
                 end_time=None, event_type=None, description=None):
        self.title = title
        self.start_date = start_date
        self.end_date = end_date
        self.start_time = start_time
        self.end_time = end_time  
        self.event_type = event_type
        self.description = description
        self.user = user


    def __repr__(self):
        return f'<Event {self.title!r}>'

