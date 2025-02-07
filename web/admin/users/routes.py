from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort
from web.admin.users.models import User
from web import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import SQLAlchemyError

bp = Blueprint('user_admin', __name__, url_prefix='/admin/user')

@bp.route('/', methods=('GET',))
def index():
    users = User.query.all()
    return render_template('admin/user/index.html', users=users, title='Users')


@bp.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        password = request.form['password']
        is_admin = request.form.get('is_admin')
        is_super = request.form.get('is_super')

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

        if not is_admin:
            is_admin = 0
        else:
            is_admin = 1
        if not is_super:
            is_super = 0
        else:
            is_super = 1
            is_admin = 1

        user = User.query.filter_by(email=email).count()
        if user > 0:
            error = f"User with {email} already exists."

        if error is None:
            user = User(first_name=first_name, 
                        last_name=last_name,
                        email=email,
                        username=username, 
                        is_admin=is_admin,
                        is_super=is_super,
                        password=password)
            
            db.session.add(user)
            db.session.commit()

            flash(f'Welcome {first_name} {last_name} your account has been successfully created.', 'success')
            return redirect(url_for("user_admin.index"))

        flash(error, 'error')
    return render_template('admin/user/create.html', title='New User')


@bp.route('/edit/<int:pk>', methods=('GET', 'POST'))
def edit(pk):
    user = User.query.get_or_404(pk)

    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        is_admin = request.form.get('is_admin')
        is_super = request.form.get('is_super')

        error = None

        if not email:
            email = user.email
        if not username:
            username = user.username
        if not first_name:
            first_name = user.first_name
        if not last_name:
            last_name = user.last_name

        if not is_admin:
            is_admin = 0
        else:
            is_admin = 1
        if not  is_super:
             is_super = 0
        else:
            is_super = 1
            is_admin = 1

        if error is None:
            
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = username
            user.password = user.password
            user.is_admin = is_admin
            user. is_super =  is_super

            db.session.add(user)
            db.session.commit()

            flash(f'User {user.first_name} {user.last_name} has been successfully updated.', 'success')
            return redirect(url_for("user_admin.index"))

        flash(error, 'error')

    return render_template('admin/user/edit.html', user=user, title=f'{user.first_name} {user.last_name}')


@bp.route('/delete/<int:pk>', methods=('GET',))
def delete(pk):
    user = User.query.get_or_404(pk)
    return render_template('admin/user/delete.html', user=user, title=f'Delete {user.first_name} {user.last_name}?')


@bp.route('/confirm_delete/<int:pk>', methods=('POST', 'GET'))
def confirm_delete(pk):
    try:
        user = User.query.get_or_404(pk)
        db.session.delete(user)
        db.session.commit()
        flash(f'The user {user.first_name} {user.last_name} has been deleted successfully!', 'success')
        return redirect(url_for('user_admin.index'))
    except SQLAlchemyError:
        db.session.rollback()
        flash(f'Could not delete this user. Try again later.', 'error')
        return(redirect(url_for('user_admin.edit', pk=user.id)))

