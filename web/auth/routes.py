import functools
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        first_name = request.form['firstname']
        last_name = request.form['lastname']
        password = request.form['password']

        error = None

        if not email:
            error = 'email is required.'
        if not username:
            username = None
        if not first_name:
            error = 'First name is required.'
        if not last_name:
            error = 'Last name is required.'
        elif not password:
            error = 'Password is required.'

        # if error is None:
        #     try:
        #        pass
        #     except db.IntegrityError:
        #         error = f"User with {email} is already registered."
        #     else:
        #         flash('Account successfully registered.')
        #         return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        error = None
        # user = db.execute(
        #     'SELECT * FROM user WHERE email = ?', (email,)
        # ).fetchone()

        # if user is None:
        #     error = 'Incorrect email.'
        # elif not check_password_hash(user['password'], password):
        #     error = 'Incorrect password.'

        # if error is None:
        #     session.clear()
        #     session['user_id'] = user['id']
        #     return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    # user_id = session.get('user_id')

    # if user_id is None:
    #     g.user = None
    # else:
    #     g.user = get_db().execute(
    #         'SELECT * FROM user WHERE id = ?', (user_id,)
    #     ).fetchone()
    pass


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view


