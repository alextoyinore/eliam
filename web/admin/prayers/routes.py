from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort
from web.admin.prayers.models import Prayer

bp = Blueprint('prayer_admin', __name__, url_prefix='/admin/prayers')

@bp.route('/', methods=('GET',))
def index():
    prayers = Prayer.query.all()
    return render_template('admin/prayers/index.html', title='Prayers Requests', prayers=prayers)

@bp.route('view/<int:pk>', methods=('GET',))
def view(pk):
    prayer = Prayer.query.get_or_404(pk)
    title = None
    if prayer.first_name is not None:
        title = f'{prayer.first_name} {prayer.last_name}'
    else:
        title = 'Anonymous'
    return render_template('admin/prayers/view.html', prayer=prayer, title=title)

# @bp.route('/create', methods=('GET', 'POST'))
# def create():
#     return render_template('admin/prayers/create.html', title='New Prayer')


