from sqlalchemy.sql import func
from web import db
from web.admin.users.models import User

# Association table
post_categories = db.Table('post_categories',
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id')),
    db.Column('category_id', db.Integer, db.ForeignKey('categories.id')))


# Association table
post_tags = db.Table('post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id')))


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), unique=True, nullable=False)
    slug = db.Column(db.String(250), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False, default='')
    excerpt = db.Column(db.Text, nullable=True)
    author = db.Column(db.Integer, nullable=False)
    co_authors = db.Column(db.Text, nullable=True)
    tags = db.Column(db.String(100), nullable=True)
    category = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    is_published = db.Column(db.Boolean, default=False, nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    publish_at = db.Column(db.DateTime(timezone=True), nullable=True)
    schedule_time = db.Column(db.DateTime(timezone=True), nullable=True)


    def __init__(self, title=None, content=None, 
                 tags=None, category=None, author=None, co_authors=None, excerpt=None, slug=None,  is_published=None):
        self.title = title
        self.content = content
        self.tags = tags
        self.category = category
        self.excerpt = excerpt
        self.author = author
        self.co_authors = co_authors
        self.is_published = is_published
        self.slug = slug

    # Tags methods

    @property
    def get_author(self):
        return User.query.get(pk=self.author)

    @property
    def get_category(self):
        return Category.query.get(pk=self.category)

    @property
    def get_tags(self):
        tags = []
        if self.tags:
            tag_names = self.tags.split(',')
            for name in tag_names:
                tag = Tag.query.filter_by(name=name.strip()).first()
                if tag:
                    tags.append(tag)
        return tags

    
    @property
    def create_tags(self):
        # Add new tags
        if self.tags:
            tag = self.tags.split(',')
            for name in self.tags:
                tag = Tag.query.filter_by(name=name.strip()).first()
                if not tag:
                    new_tag = Tag(name=name.strip(), slug=name.replace(' ', '-'))
                    db.session.add(new_tag)
            db.session.commit()


    @property
    def get_co_authors(self):
        co_authors = []
        if self.co_authors:
            co_authors_usernames = self.co_authors.split(',')
            for username in co_authors_usernames:
                author = User.query.filter_by(username=username.strip())
                if author:
                    co_authors.append(author)
        return co_authors

    def __repr__(self):
        return f'<User {self.title!r}>'


class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    slug = db.Column(db.String(80), nullable=False, unique=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    

    def __init__(self, name=None, slug=None):
        self.name = name
        self.slug = slug

    def __repr__(self):
        return f'<Tag {self.name!r}>'


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    slug = db.Column(db.String(80), nullable=False, unique=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())


    def __init__(self, name=None, slug=None, description=None):
        self.name = name
        self.description = description
        self.slug = slug

    def __repr__(self):
        return f'<Category {self.name!r}>'


