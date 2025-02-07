from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort
from web.decorators import login_required


bp = Blueprint('event_admin', __name__, url_prefix='/admin/event')


@bp.route('/', methods=('GET',))
@login_required(['admin', 'super', 'contributor'])
def index():
    return render_template('admin/events/index.html', title='Events')


@bp.route('/create', methods=('GET', 'POST'))
@login_required(['admin', 'super', 'contributor'])
def create():
    return render_template('admin/events/create.html', title='New Event')


@bp.route('/edit/<int:pk>', methods=('GET', 'PATCH'))
@login_required(['admin', 'super', 'contributor'])
def edit(pk):
    return render_template('admin/events/edit.html')


@bp.route('/delete/<int:pk>', methods=('DELETE',))
def delete(pk):
    pass

