from flask import Blueprint, flash, session, g, redirect, render_template, request, url_for
from datetime import datetime, timedelta
from web import db
from werkzeug.exceptions import abort
from werkzeug.security import generate_password_hash, check_password_hash
from web.admin.users.models import User
from web.context import is_authenticated

bp = Blueprint('auth_admin', __name__, url_prefix='/admin/auth')

@bp.route('/', methods=('GET', 'POST'))
def index():
    if is_authenticated():
        return redirect(url_for('admin.index'))

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        error = None

        # Check if user exists
        user = User.query.filter_by(email=email).first()

        if user is None:
            error = f'There is no account with the email: {email}'
        else:
            if user.check_password(password):
                session['user_id'] = user.id
                session['user_role'] = user.role
                session['login_time'] = datetime.now().isoformat()
                session['fresh_login'] = True
                next_page = session.pop('next', None)
                flash(f'Welcome {user.last_name}', 'success')
                return redirect(next_page or url_for('admin.index'))
            else:
                error = f'The password provided does not match the account'
        flash(error, 'error')
    return render_template('admin/auth/index.html', title='Log in')


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth_admin.index'))


@bp.route('/password-recovery', methods=('GET', 'POST'))
def forgot_password():
    return render_template('admin/auth/forgot_password.html')

