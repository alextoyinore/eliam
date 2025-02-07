from web import create_app
from flask import g
from web.context import get_current_user

app = create_app()

@app.before_request
def before_request():
    g.user = get_current_user()

@app.context_processor
def utility_processor():
    def is_authenticated():
        return get_current_user() is not None
        
    def current_user():
        return get_current_user()
        
    return {
        'is_authenticated': is_authenticated,
        'current_user': current_user
    }

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

