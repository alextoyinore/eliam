from flask import Blueprint, flash, g, session, redirect, render_template, request, url_for
from werkzeug.exceptions import abort
from web import db
from web.admin.hymns.models import Hymn
from web.admin.hymns.forms import HymnForm
from web.admin.users.models import User
from sqlalchemy.exc import SQLAlchemyError, IntegrityError


bp = Blueprint('hymns_admin', __name__, url_prefix='/admin/hymns')


@bp.route('/', methods=('GET',))
def index():
    hymns = Hymn.query.all()
    for hymn in hymns:
        hymn.user = User.query.get_or_404(hymn.user).fullname
    return render_template('admin/hymns/index.html', hymns=hymns, title='Hymns')


@bp.route('/create', methods=('GET', 'POST'))
def create():
    form = HymnForm()
    error = None
    if request.method == 'POST':
        try:
            title = request.form['title']
            slug = title.replace(' ', '-')
            content = request.form['content']
            user = session['user_id']

            hymn = Hymn(title=title, slug=slug,content=content,user=user)
            db.session.add(hymn)
            db.session.commit()

            flash(f'Your hymn {title} has been created successfully.', 'success')

            return redirect(url_for('hymns_admin.index'))

        except IntegrityError:
            db.session.rollback()
            error = f'An hymn with the title {title} already exists'

        except SQLAlchemyError as e:
            db.session.rollback()
            error = f'An error occured while creating your hymn'

        flash(error, 'error')
    return render_template('admin/hymns/create.html', form=form, title='New Hymn')


@bp.route('/edit/<int:pk>', methods=('GET', 'POST'))
def edit(pk):
    form = HymnForm()
    hymn = Hymn.query.get_or_404(pk)
    error = None
    if request.method == 'POST':
        try:
            title = request.form['title']
            slug = title.replace(' ', '-')
            content = request.form['content']

            hymn.title = title
            hymn.slug = slug
            hymn.content = content

            db.session.add(hymn)
            db.session.commit()

            flash(f'Your hymn {title} has been updated successfully.', 'success')

            return redirect(url_for('hymns_admin.index'))

        except IntegrityError:
            db.session.rollback()
            error = f'An hymn with the title {title} already exists'

        except SQLAlchemyError as e:
            db.session.rollback()
            error = f'An error occured while updating your hymn'
            
        flash(error, 'error')

    return render_template('admin/hymns/edit.html', form=form, hymn=hymn, title=hymn.title)



@bp.route('/delete/<int:pk>', methods=('GET',))
def delete(pk):
    event = Hymn.query.get_or_404(pk)
    return render_template('admin/hymn/delete.html', event=event, title=event.title)


@bp.route('/confirm_delete/<int:pk>', methods=('POST', 'GET'))
def confirm_delete(pk):
    try:
        hymn = Hymn.query.get_or_404(pk)
        db.session.delete(hymn)
        db.session.commit()
        flash(f'The hymn {hymn.title} has been deleted successfully!', 'success')
        return redirect(url_for('hymn_admin.delete'))
        
    except SQLAlchemyError:
        db.session.rollback()
        flash(f'Could not delete this hymn. Try again later.', 'error')
        return(redirect(url_for('hymn_admin.edit', pk=hymn.id)))


