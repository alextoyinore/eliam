from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort
# from web.auth.auth import login_required
# from web.db import get_db

bp = Blueprint('blog', __name__, url_prefix='/blog')

@bp.route('/blog/<int:pk>')
def view(article):
    return render_template('pages/blog/index.html', article=article)

@bp.route('/blog')
def index():
    return render_template('pages/blog/index.html')

