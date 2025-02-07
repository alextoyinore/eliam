from flask import Blueprint, flash, g, session, redirect, render_template, request, url_for
from werkzeug.exceptions import abort
from web.admin.notices.models import Notice
from web.admin.users.models import User
from sqlalchemy.exc import SQLAlchemyError
from web import db


bp = Blueprint('notices_admin', __name__, url_prefix='/admin/notices')

@bp.route('/', methods=('GET',))
def index():
    notices = Notice.query.all()
    for notice in notices:
        user = User.query.get_or_404(notice.user)
        notice.user = user
    return render_template('admin/notices/index.html', title='Notices', notices=notices)

@bp.route('/create', methods=('GET', 'POST'))
def create():
    error = None
    if request.method == 'POST':
        try:
            title = request.form['title'].strip()
            content = request.form['content'].strip()
            notice = Notice(title=title, content=content, user=session['user_id'])
            db.session.add(notice)
            db.session.commit()
            flash('Your notice has been successfully created', 'success')
            return redirect(url_for('notices_admin.index'))
        except SQLAlchemyError:
            db.session.rollback()
            error = f"There's been an issue creating your new notice. Kindly try again later"
        flash(error, 'error')
    return render_template('admin/notices/create.html', title='New Notice')


@bp.route('/edit/<int:pk>', methods=('GET', 'POST'))
def edit(pk):
    notice = Notice.query.get_or_404(pk)

    error = None

    if request.method == 'POST':
        try:
            title = request.form['title'].strip()
            content = request.form['content'].strip()

            if notice.title == title and notice.content == content:
                flash('No changes made', 'info')
                return redirect(url_for('notices_admin.index'))
            else:
                notice.title = title
                notice.content = content
                db.session.add(notice)
                db.session.commit()

                flash(f'Notice: {notice.title} has been successfully updated.', 'success')
                return redirect(url_for("notices_admin.index"))
                
        except SQLAlchemyError:
            db.session.rollback()
            error = f'There has been an issue updating your notice. Kindly try again later.'
        flash(error, 'error')

    return render_template('admin/notices/edit.html', notice=notice, title=f'{notice.title}')


@bp.route('/delete/<int:pk>', methods=('GET',))
def delete(pk):
    notice = Notice.query.get_or_404(pk)
    return render_template('admin/notices/delete.html', notice=notice, title=f'Delete {notice.title}?')


@bp.route('/confirm_delete/<int:pk>', methods=('POST', 'GET'))
def confirm_delete(pk):
    try:
        notice = Notice.query.get_or_404(pk)
        db.session.delete(notice)
        db.session.commit()
        flash(f'The notice {notice.title} has been deleted successfully!', 'success')
        return redirect(url_for('notices_admin.index'))
    except SQLAlchemyError:
        db.session.rollback()
        flash(f'Could not delete this user. Try again later.', 'error')
        return(redirect(url_for('notices_admin.edit', pk=notice.id)))

