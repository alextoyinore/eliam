from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort
# from web.auth.auth import login_required
# from web.db import get_db

bp = Blueprint('enquiry', __name__, url_prefix='/enquiry')

@bp.route('/create', methods=('GET', 'POST'))
def create():
    return render_template('admin/enquiries/create.html')

