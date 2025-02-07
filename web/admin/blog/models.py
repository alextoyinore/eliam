from sqlalchemy.sql import func
from web import db

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
    author = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), name='post_author', nullable=False)
    co_authors = db.Column(db.Text, nullable=True)
    tags = db.relationship('Tag', secondary=post_tags, backref='posts')
    categories = db.relationship('Category', secondary=post_categories, backref='posts')
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    is_published = db.Column(db.Boolean, default=False, nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    publish_at = db.Column(db.DateTime(timezone=True), nullable=True)
    schedule_time = db.Column(db.DateTime(timezone=True), nullable=True)


    def __init__(self, title=None, content=None, 
                 tags=None, categories=None, author=None, co_authors=None, excerpt=None, slug=None,  is_published=None):
        self.title = title
        self.content = content
        self.tags = tags
        self.categories = categories
        self.excerpt = excerpt
        self.author = author
        self.co_authors = co_authors
        self.is_published = is_published
        self.slug = slug

    # Tags methods
    
    @property
    def tag_list(self):
        return [tag.name for tag in self.tags]
    
    @tag_list.setter
    def tag_list(self, tag_names):
        # Clear existing tags
        self.tags = []
        # Add new tags
        for name in tag_names:
            tag = Tag.query.filter_by(name=name).first()
            if tag:
                self.tags.append(tag)
    
    @property
    def tag_ids(self):
        return [tag.id for tag in self.tags]
    
    # Optional: Get as comma-separated string
    @property
    def tag_string(self):
        return ', '.join(self.tag_list) 

    @property
    def get_co_authors(self):
        return self.co_authors.split(',') if self.co_authors else []
    
    # Categories Methods
    
    @property
    def category_list(self):
        return [cat.name for cat in self.categories]
    
    @category_list.setter
    def category_list(self, category_names):
        # Clear existing tags
        self.categories = []
        # Add new categories
        for name in category_names:
            category = Category.query.filter_by(name=name).first()
            if category:
                self.categories.append(category)
    
    @property
    def category_ids(self):
        return [cat.id for cat in self.categories]

    @property
    def category_string(self):
        return ', '.join(self.category_list)

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


