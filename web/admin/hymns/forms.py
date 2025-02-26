from flask_wtf import FlaskForm
from wtforms import *

class HymnForm(FlaskForm):
    title = StringField(name='title', id='title', render_kw={
        'placeholder':'Title', 
        'class':"w-full py-2 px-3 border focus:outline-sky-500"
        })

    content = TextAreaField(name='content', id='content', render_kw={
        'placeholder':'Content', 
        'class':"w-full min-h-[450px] py-2 px-3 border focus:outline-sky-500"
        })

