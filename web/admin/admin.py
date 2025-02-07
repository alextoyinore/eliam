import functools
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from web.decorators import login_required

bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.route('/')
@login_required(['admin', 'super', 'contributor'])
def index():
    return render_template('admin/index.html', title='Admin')

# @bp.route('/delete/<int:pk>/<obj>')
# def delete(pk, obj):
#     return render_template('admin/delete.html', title='Delete', obj=obj)

