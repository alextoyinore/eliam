from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort
# from web.auth.auth import login_required
# from web.db import get_db

bp = Blueprint('bible', __name__, url_prefix='/bible')

@bp.route('/', methods=('GET',))
def index():
    return render_template('features/bible/index.html')

@bp.route('/books', methods=('GET',))
def books():
    return render_template('features/bible/books.html')

# Select Chapter
@bp.route('<book>/', methods=('GET',))
def chapters(book):
    return render_template('features/bible/chapters.html', book=book)

# Select Verse
@bp.route('<book>/<int:chapter>', methods=('GET',))
def verses(book, chapter):
    return render_template('features/bible/verses.html', book=book, chapter=chapter)

# Read a verse
@bp.route('<book>/<int:chapter>/<int:verse>', methods=('GET',))
def read(book, chapter, verse):
    return render_template('features/bible/read.html', book=book, chapter=chapter, verse=verse)

