from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort


bp = Blueprint('gallery_admin', __name__, url_prefix='/admin/gallery')

@bp.route('/', methods=('GET',))
def index():
    return render_template('admin/gallery/index.html', title='Gallery')

@bp.route('/create', methods=('GET', 'POST'))
def create():
    return render_template('admin/gallery/create.html', title='New Photobook')

@bp.route('/edit/<int:pk>', methods=('GET', 'PATCH'))
def edit(pk):
    return render_template('admin/gallery/edit.html')

@bp.route('/delete/<int:pk>', methods=('DELETE',))
def delete(pk):
    pass

