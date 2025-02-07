import os

from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


DEV_KEY = 'dev'
DB_FILE_NAME = 'dev.db'

db = SQLAlchemy()
migrate = Migrate()


def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY=DEV_KEY)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, DB_FILE_NAME)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


    if test_config is None:
        # Load the instance file if exists when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load test config if passed in
        app.config.from_mapping(test_config)
    
    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Landing Page
    @app.route('/')
    def index():
        # return 'This is homepage'
        return render_template('site/index.html')
    
    @app.route('/back')
    def back():
        next_page = request.args.get('next')
        return redirect(next_page or url_for('default_route'))
    

    # from . import db
    db.init_app(app)
    # Migrate
    migrate.init_app(app, db)

    # Import models
    from web.admin.users.models import User
    from web.admin.blog.models import Post, Tag, Category
    from web.admin.enquiries.models import Enquiry
    from web.admin.events.models import Event
    from web.admin.forum.models import Forum, ForumMessage
    from web.admin.gallery.models import Photobook
    from web.admin.hymns.models import Hymn
    from web.admin.members.models import Member
    from web.admin.notices.models import Notice
    from web.admin.prayers.models import Prayer
    from web.admin.sermon.models import Sermon
    from web.admin.testimony.models import Testimony
    from web.admin.training.models import Training


    # Blueprints
    from web.auth import routes as auth

    from web.site import blog
    from web.site import bible
    from web.site import enquiry

    # Admin Routes Imports
    from web.admin import admin
    from web.admin.blog import routes as blog_admin
    from web.admin.events import routes as event_admin
    from web.admin.enquiries import routes as enquiries_admin
    from web.admin.gallery import routes as gallery_admin
    from web.admin.hymns import routes as hymns_admin
    from web.admin.forum import routes as forum_admin
    from web.admin.notices import routes as notices_admin
    from web.admin.testimony import routes as testimony_admin
    from web.admin.services import routes as service_admin
    from web.admin.sermon import routes as sermon_admin
    from web.admin.training import routes as training_admin
    from web.admin.prayers import routes as prayer_admin
    from web.admin.members import routes as member_admin
    from web.admin.users import routes as user_admin
    from web.admin.auth import routes as auth_admin

    # Blueprints

    # Authentication Blueprint
    app.register_blueprint(auth.bp)

    # Front Blueprint
    app.register_blueprint(blog.bp)
    app.register_blueprint(bible.bp)
    app.register_blueprint(enquiry.bp)

    # Admin Blueprint
    app.register_blueprint(admin.bp)
    app.register_blueprint(blog_admin.bp)
    app.register_blueprint(event_admin.bp)
    app.register_blueprint(enquiries_admin.bp)
    app.register_blueprint(gallery_admin.bp)
    app.register_blueprint(hymns_admin.bp)
    app.register_blueprint(forum_admin.bp)
    app.register_blueprint(notices_admin.bp)
    app.register_blueprint(testimony_admin.bp)
    app.register_blueprint(service_admin.bp)
    app.register_blueprint(sermon_admin.bp)
    app.register_blueprint(training_admin.bp)
    app.register_blueprint(prayer_admin.bp)
    app.register_blueprint(member_admin.bp)
    app.register_blueprint(user_admin.bp)
    app.register_blueprint(auth_admin.bp)

    return app
    
