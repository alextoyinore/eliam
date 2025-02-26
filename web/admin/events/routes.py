from flask import Blueprint, flash, g, session, redirect, render_template, request, url_for
from datetime import datetime, date, time
from web import db
from werkzeug.exceptions import abort
from web.decorators import login_required
from .forms import EventForm
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from .models import Event

bp = Blueprint('event_admin', __name__, url_prefix='/admin/event')


@bp.route('/', methods=('GET',))
@login_required(['admin', 'super', 'contributor'])
def index():
    events = Event.query.all()
    return render_template('admin/events/index.html', events=events, title='Events')


@bp.route('/create', methods=('GET', 'POST'))
@login_required(['admin', 'super', 'contributor'])
def create():
    form = EventForm()
    error = None
    if request.method == 'POST':
        try:
            title = request.form['title'].strip()
            start_date = request.form.get('start_date')
            end_date = request.form.get('end_date')
            start_time = request.form.get('start_time')
            end_time = request.form.get('end_time')
            description = request.form['description']
            user = session['user_id']
            event_type = request.form.get('event_type')

            # print(f'Start Date: {start_date}')

            st_date_list = start_date.split('-')
            start_date = date(int(st_date_list[0]), int(st_date_list[1]), int(st_date_list[2]))

            en_date_list = end_date.split('-')
            end_date = date(int(en_date_list[0]), int(en_date_list[1]), int(en_date_list[2]))

            st_time_list = start_time.split(':')
            start_time = time(int(st_time_list[0]), int(st_time_list[1]))

            en_time_list = end_time.split(':')
            end_time = time(int(en_time_list[0]), int(en_time_list[1]))
            
            event = Event(title=title, 
            start_date=start_date, 
            end_date=end_date, 
            start_time=start_time, 
            end_time=end_time, 
            description=description, 
            user=user, 
            event_type=event_type)

            db.session.add(event)
            db.session.commit()

            flash(f'Event {title} has been successfully created', 'success')
            return redirect(url_for('event_admin.index'))
        
        except IntegrityError:
            db.session.rollback()
            error = f'Event with title {title} already exists'
            flash(error, 'error')

        except SQLAlchemyError as e:
            db.session.rollback()
            error = f'An error occured while creating your event {e._message}'
            flash(error, 'error')
    
    return render_template('admin/events/create.html', form=form, title='New Event')


@bp.route('/edit/<int:pk>', methods=('GET', 'POST'))
@login_required(['admin', 'super', 'contributor'])
def edit(pk):
    form = EventForm()
    event = Event.query.get_or_404(pk)
    # event.start_date = event.start_date
    if request.method == 'POST':
        try:
            title = request.form['title'].strip()
            start_date = request.form.get('start_date')
            end_date = request.form.get('end_date')
            start_time = request.form.get('start_time')
            end_time = request.form.get('end_time')
            description = request.form['description']
            event_type = request.form.get('event_type')

            # print(f'Start Date: {start_date}')

            st_date_list = start_date.split('-')
            start_date = date(int(st_date_list[0]), int(st_date_list[1]), int(st_date_list[2]))

            en_date_list = end_date.split('-')
            end_date = date(int(en_date_list[0]), int(en_date_list[1]), int(en_date_list[2]))

            st_time_list = start_time.split(':')
            start_time = time(int(st_time_list[0]), int(st_time_list[1]))

            en_time_list = end_time.split(':')
            end_time = time(int(en_time_list[0]), int(en_time_list[1]))
            
            event.title = title
            event.start_date = start_date
            event.end_date = end_date
            event.start_time = start_time
            event.end_time = end_time
            event.event_type = event_type
            event.description = description

            db.session.add(event)
            db.session.commit()

            flash(f'Event {title} has been successfully updated', 'success')
            return redirect(url_for('event_admin.index'))
        
        except IntegrityError:
            db.session.rollback()
            error = f'Event with title {title} already exists'
            flash(error, 'error')

        except SQLAlchemyError as e:
            db.session.rollback()
            error = f'An error occured while updating your event {e._message}'
            flash(error, 'error')

    return render_template('admin/events/edit.html', event=event, form=form, title=event.title)


@bp.route('/delete/<int:pk>', methods=('GET',))
def delete(pk):
    event = Event.query.get_or_404(pk)
    return render_template('admin/events/delete.html', event=event, title=event.title)


@bp.route('/confirm_delete/<int:pk>', methods=('POST', 'GET'))
def confirm_delete(pk):
    try:
        event = Event.query.get_or_404(pk)
        db.session.delete(event)
        db.session.commit()
        flash(f'The event {event.title} has been deleted successfully!', 'success')
        return redirect(url_for('event_admin.index'))
    except SQLAlchemyError:
        db.session.rollback()
        flash(f'Could not delete this event. Try again later.', 'error')
        return(redirect(url_for('event_admin.edit', pk=event.id)))

