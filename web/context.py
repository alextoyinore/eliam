from flask import session, g
from web.admin.users.models import User

def get_current_user():
    if not hasattr(g, 'current_user'):
        if 'user_id' in session:
            g.current_user = User.query.get(session['user_id'])
        else:
            g.current_user = None
    return g.current_user


def is_authenticated():
        return get_current_user() is not None

