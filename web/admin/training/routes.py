from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort

bp = Blueprint('training_admin', __name__, url_prefix='/admin/training')

@bp.route('/', methods=('GET',))
def index():
    return render_template('admin/training/index.html', title='Trainings')

@bp.route('/create', methods=('GET', 'POST'))
def create():
    return render_template('admin/training/create.html', title='New Training')

@bp.route('/edit/<int:pk>', methods=('GET', 'PATCH'))
def edit(pk):
    return render_template('admin/training/edit.html')

@bp.route('/delete/<int:pk>', methods=('DELETE',))
def delete(pk):
    pass

