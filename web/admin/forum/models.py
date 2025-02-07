from sqlalchemy.sql import func
from web import db

class Forum(db.Model):
    __tablename__ = 'forums'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    def __init__(self, user=None, title=None, description=None):
        self.user = user
        self.title = title
        self.description = description

    def __repr__(self):
        return f'<Notice {self.title!r} {self.description!r}>'


class ForumMessage(db.Model):
    __tablename__ = 'forum_messages'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    forum = db.Column(db.Integer, nullable=False)
    member = db.Column(db.Integer, nullable=False)
    message_id = db.Column(db.Integer, nullable=True)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    def __init__(self, member=None, forum=None, message_id=None, message=None):
        self.forum = forum
        self.member = member
        self.message_id = message_id
        self.message = message

    def __repr__(self):
        return f'<Notice {self.forum!r} {self.member!r} {self.message}>'
    
