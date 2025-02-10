from flask import Blueprint, flash, g, session, redirect, render_template, request, url_for
from web import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from werkzeug.exceptions import abort
from flask import jsonify
from .models import Tag, Category, Post
from .forms import PostForm, CategoryForm, TagForm
from web.admin.users.models import User


bp = Blueprint('blog_admin', __name__, url_prefix='/admin/blog')

@bp.route('/', methods=('GET',))
def index():
    posts = Post.query.all()
    for post in posts:
        cat = Category.query.get(post.category).name
        post.category = cat
        author = User.query.get(post.author).fullname
        post.author = author
    return render_template('admin/blog/index.html', posts=posts, title='Posts')


@bp.route('/create', methods=('GET', 'POST'))
def create():
    form = PostForm()
    if request.method == 'POST':
        try:
            
            title = request.form['title'].strip()
            slug = title.replace(' ', '-')
            content = request.form['content'].strip()
            excerpt = request.form['excerpt'].strip()
            co_authors = request.form['co_authors'].strip()
            tags = request.form['tags'].strip()
            category = int(request.form['category'])
            author = session['user_id']
            is_published = request.form.get('is_published')

            error = None

            if not title:
                error = 'Title is required.'
            

            if error is None:
                post = Post(title=title, 
                            slug=slug,
                            content=content,
                            author=author,
                            excerpt=excerpt, 
                            co_authors=co_authors,
                            tags=tags,
                            category=category,
                            is_published=is_published)
                db.session.add(post)
                db.session.commit()

                # post.create_tags()

                flash(f'{title} has been published successfully!', 'success')
                return redirect(url_for("user_admin.index"))
        
        except IntegrityError:
            db.session.rollback()
            error = f'A post with that title {title} already exists.'
            
        except SQLAlchemyError as e:
            db.session.rollback()
            error = f'An error occured while saving your post. Try again later. {e._message}'
            
        flash(error, 'error')
    return render_template('admin/blog/create.html', title='New Blog', form=form)


@bp.route('/edit/<int:pk>', methods=('GET', 'POST'))
def edit(pk):
    form = PostForm()
    post = Post.query.get_or_404(pk)
    return render_template('admin/blog/edit.html', title=post.title, form=form, post=post)


@bp.route('/delete/<int:pk>', methods=('POST',))
def delete(pk):
    post = Post.query.get_or_404(pk)
    return render_template('admin/blog/tag/delete.html', post=post, title=post.title)


@bp.route('/confirm_delete/<int:pk>', methods=('POST', 'GET'))
def confirm_delete(pk):
    try:
        post = Post.query.get_or_404(pk)
        db.session.delete(post)
        db.session.commit()
        flash(f'The tag {post.title} has been deleted successfully!', 'success')
        return redirect(url_for('blog_admin.tags'))
    except SQLAlchemyError:
        db.session.rollback()
        flash(f'Could not delete this post. Try again later.', 'error')
        return(redirect(url_for('blog_admin.edit', pk=post.id)))



# Tag routes
@bp.route('/tags', methods=('GET',))
def tags():
    tags = Tag.query.all()
    return render_template('admin/blog/tag/index.html', title='Tags', tags=tags)


@bp.route('/tag/create', methods=('GET', 'POST'))
def create_tag():
    if request.method == 'POST':
        name = request.form['name']
    
        error = None
        
        if not name:
            error = 'Name is required'
        
        if error is None:
            try:
                slug = name.replace(' ', '-') or name                
                tag = Tag(name=name, slug=slug)
                db.session.add(tag)
                db.session.commit()
                flash(f'Tag {name} has been succesfully created', 'success')
                return redirect(request.referrer or url_for('blog_admin.index'))
            except IntegrityError as e:
                db.session.rollback()
                error = f'A tag with the name {name} already exists'
            except SQLAlchemyError as e:
                db.session.rollback()
                error = 'There was an error creating the tag'
            flash(error, 'error')
    return render_template('admin/blog/tag/create.html', title='New Tag', form=TagForm())


@bp.route('/tag/edit/<int:pk>', methods=('GET', 'POST'))
def edit_tag(pk):
    tag = Tag.query.get_or_404(pk)
    
    error = None
    
    if request.method == 'POST':
        try:
            name = request.form['name']
            tag.name = name
            db.session.add(tag)
            db.session.commit()
            flash(f'{tag.name} has been successfully update', 'success')
        except SQLAlchemyError:
            db.session.rollback()
            error = f'There was an error updating the tag "{tag.name}"'
        flash(error, 'error')
    return render_template('admin/blog/tag/edit.html', tag=tag, title=tag.name, form=TagForm())


@bp.route('/tag/delete/<int:pk>', methods=('GET',))
def delete_tag(pk):
    tag = Tag.query.get_or_404(pk)
    return render_template('admin/blog/tag/delete.html', tag=tag, title=tag.name)


@bp.route('/tag/confirm_delete/<int:pk>', methods=('GET', 'POST'))
def confirm_delete_tag(pk):
    try:
        tag = Tag.query.get_or_404(pk)
        db.session.delete(tag)
        db.session.commit()
        flash(f'The tag {tag.name} has been deleted successfully!', 'success')
        return redirect(url_for('blog_admin.tags'))
    except SQLAlchemyError:
        db.session.rollback()
        flash(f'Could not delete this tag. Try again later.', 'error')
        return(redirect(url_for('blog_admin.edit_tag', pk=tag.id)))


# Get Tags
@bp.route('api/tags')
def get_tags():
    tags = Tag.query.all()
    return jsonify([tag.name for tag in tags])



# Category routes
@bp.route('/categories', methods=('GET',))
def categories():
    categories = Category.query.all()
    return render_template('admin/blog/category/index.html', title='Categories', categories=categories)


@bp.route('/category/create', methods=('GET', 'POST'))
def create_category():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
    
        error = None
        
        if not name:
            error = 'Name is required'
        
        if error is None:
            try:
                slug = name.replace(' ', '-') or name                
                category = Category(name=name, description=description, slug=slug)
                db.session.add(category)
                db.session.commit()
                flash(f'Category {name} has been succesfully created', 'success')
                return redirect(request.referrer or url_for('blog_admin.index'))
            except IntegrityError as e:
                db.session.rollback()
                error = f'A category with the name {name} already exists'
            except SQLAlchemyError as e:
                db.session.rollback()
                error = 'There was an error creating the category'
            flash(error, 'error')
    return render_template('admin/blog/category/create.html', title='New Category', form=CategoryForm())


@bp.route('/category/edit/<int:pk>', methods=('GET', 'POST'))
def edit_category(pk):
    category = Category.query.get_or_404(pk)
    
    error = None
    
    if request.method == 'POST':
        try:
            name = request.form['name']
            description = request.form['description']
            category.name = name
            category.description = description
            db.session.add(category)
            db.session.commit()
            flash(f'{category.name} has been successfully update', 'success')
        except SQLAlchemyError:
            db.session.rollback()
            error = f'There was an error updating the category "{category.name}"'
        flash(error, 'error')
    return render_template('admin/blog/category/edit.html', category=category, form=CategoryForm())


@bp.route('/category/delete/<int:pk>', methods=('GET',))
def delete_category(pk):
    category = Category.query.get_or_404(pk)
    return render_template('admin/blog/category/delete.html', category=category, title=category.name)


@bp.route('/category/confirm_delete/<int:pk>', methods=('POST', 'GET'))
def confirm_delete_category(pk):
    try:
        category = Category.query.get_or_404(pk)
        db.session.delete(category)
        db.session.commit()
        flash(f'The category {category.name} has been deleted successfully!', 'success')
        return redirect(url_for('blog_admin.categories'))
    except SQLAlchemyError:
        db.session.rollback()
        flash(f'Could not delete this category. Try again later.', 'error')
        return(redirect(url_for('blog_admin.edit_category', pk=category.id)))


# Get categories
@bp.route('api/categories')
def get_categories():
    categories = Category.query.all()
    return jsonify([category.name for category in categories])

