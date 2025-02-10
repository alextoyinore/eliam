from flask_wtf import FlaskForm
from wtforms import *
# from .models import Category, Tag


class EventForm(FlaskForm):
    title = StringField(name='title', id='title', render_kw={
        'placeholder':'Title', 
        'class':"w-[80%] py-1 px-3 border focus:outline-sky-500"
        })
    
    start_date = DateField(name='start_date', id='start_date', render_kw={
        'placeholder':'Start Date', 
        'class':"w-[80%] py-1 px-3 border focus:outline-sky-500"
        })

    end_date = DateField(name='end_date', id='end_date', render_kw={
        'placeholder':'End Date', 
        'class':"w-[80%] py-1 px-3 border focus:outline-sky-500"
        })

    start_time = TimeField(name='start_time', id='start_time', render_kw={
        'placeholder':'Start Time', 
        'class':"w-[80%] py-1 px-3 border focus:outline-sky-500"
        })

    end_time = TimeField(name='end_time', id='end_time', render_kw={
        'placeholder':'Start Time', 
        'class':"w-[80%] py-1 px-3 border focus:outline-sky-500"
        })

    description = TextAreaField(name='description', id='description', render_kw={
        'class':"w-[80%] min-h-[100px] py-1 px-3 border focus:outline-sky-500"
        })
    
    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        # Populate choices
        # self.categories.choices = [(c.id, c.name) for c in Category.query.all()]
        # self.tags.choices = [(t.id, t.name) for t in Tag.query.all()]

