from functools import wraps
from flask import session, redirect, url_for, flash, request, abort
from datetime import datetime, timedelta

def login_required(roles=None, fresh_login=False):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Check if user is logged in
            if 'user_id' not in session:
                session['next'] = request.url
                flash('Please log in to access this page.')
                return redirect(url_for('auth_admin.index'))
            
            # Check session expiry
            if 'login_time' in session:
                login_time = datetime.fromisoformat(session['login_time'])
                if datetime.now() - login_time > timedelta(hours=24):
                    session.clear()
                    flash('Your session has expired. Please log in again.')
                    return redirect(url_for('auth_admin.index'))
            
            # Check if fresh login required
            if fresh_login and 'fresh_login' not in session:
                session['next'] = request.url
                flash('Please log in again to access this page.')
                return redirect(url_for('auth_admin.index'))
            
            # Check roles
            if roles:
                user_role = session.get('user_role')
                if user_role not in roles:
                    flash('You do not have permission to access this page.')
                    return abort(403)
            
            return f(*args, **kwargs)
        return decorated_function
    
    if callable(roles):
        fn = roles
        roles = None
        return decorator(fn)
    return decorator



