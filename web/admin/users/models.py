from sqlalchemy.sql import func
from web import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(120), unique=True, nullable=True)
    password = db.Column(db.String(50), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    is_super = db.Column(db.Boolean, default=False, nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    

    @property
    def fullname(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def initials(self):
        return f'{self.first_name[0]}{self.last_name[0]}'

    @property
    def role(self):
        if self.is_super:
            return 'super'
        elif not self.is_super and self.is_admin:
            return 'admin'
        else:
            return 'contributor'
        
    @property
    def is_authenticated(self):
        return True

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __init__(self, first_name=None, last_name=None, 
                 email=None, username=None, password=None, is_admin=None, is_super=None):
        if int(is_super) == 1:
            is_admin = 1 
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.username = username
        self.password = generate_password_hash(password)   
        self.is_admin = is_admin
        self.is_super = is_super

    def __repr__(self):
        return f'<User {self.first_name!r} {self.last_name!r}>'

