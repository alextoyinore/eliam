from flask_wtf import FlaskForm
from wtforms import *
from .models import Category, Tag

class CategoryForm(FlaskForm):
    name = StringField(name='name', id='name', render_kw={
        'placeholder':'Name', 
        'class':"w-full py-2 px-3 border focus:outline-sky-500"
        })
    description = TextAreaField(name='description', id='description', render_kw={
        'placeholder': 'Description',
        'class':"w-full min-h-[150px] py-1 px-3 border focus:outline-sky-500"
        })


class TagForm(FlaskForm):
    name = StringField(name='name', id='name', render_kw={
        'placeholder':'Title', 
        'class':"w-full py-2 px-3 border focus:outline-sky-500"
        })


class PostForm(FlaskForm):
    title = StringField(name='title', id='title', render_kw={
        'placeholder':'Title', 
        'class':"w-full py-2 px-3 border focus:outline-sky-500"
        })
    content = TextAreaField(name='content', id='editor', render_kw={
        'class':"w-full min-h-[500px] py-1 px-3 border focus:outline-sky-500"
        })
    excerpt = TextAreaField(name='excerpt', id='excerpt', render_kw={
        'placeholder':'Excerpt',
        'class':"w-full min-h-[100px] py-1 px-3 border focus:outline-sky-500"
        })
    co_authors = SearchField(name='co_authors', id='co_authors', render_kw={
        'placeholder':'Co-Authors',
        'class':"w-full py-2 px-3 border focus:outline-sky-500"
        })
    tags = StringField(name='tags', id='tagInput', render_kw={
        'placeholder':'Tags',
        'class':"w-full py-2 px-3 border focus:outline-sky-500 form-control"
        })
    categories = SelectMultipleField(name='categories', id='categories', coerce=int, render_kw={'placeholder':'Category', 'class':"w-full py-2 px-3 border focus:outline-sky-500 form-control"
        })
    
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        # Populate choices
        self.categories.choices = [(c.id, c.name) for c in Category.query.all()]
        self.tags.choices = [(t.id, t.name) for t in Tag.query.all()]
        
