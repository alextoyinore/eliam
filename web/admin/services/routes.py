from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort
# from web.auth.auth import login_required
# from web.db import get_db

bp = Blueprint('service_admin', __name__, url_prefix='/admin/services')

@bp.route('/', methods=('GET',))
def index():
    return render_template('admin/services/index.html', title='Services')

@bp.route('/create', methods=('GET', 'POST'))
def create():
    return render_template('admin/services/create.html', title='New Service')

@bp.route('/edit/<int:pk>', methods=('GET', 'PATCH'))
def edit(pk):
    return render_template('admin/services/edit.html')

@bp.route('/delete/<int:pk>', methods=('DELETE',))
def delete(pk):
    pass

