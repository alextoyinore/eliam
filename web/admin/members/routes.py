from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort
# from web.auth.auth import login_required
# from web.db import get_db

bp = Blueprint('member_admin', __name__, url_prefix='/admin/members')

@bp.route('/', methods=('GET',))
def index():
    return render_template('admin/member/index.html', title='Members')

@bp.route('/create', methods=('GET', 'POST'))
def create():
    return render_template('admin/member/create.html', title='New Member')

@bp.route('/edit/<int:pk>', methods=('GET', 'PATCH'))
def edit(pk):
    return render_template('admin/member/edit.html')

@bp.route('/delete/<int:pk>', methods=('DELETE',))
def delete(pk):
    pass

