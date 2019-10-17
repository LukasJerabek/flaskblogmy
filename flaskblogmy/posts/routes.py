
from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskblogmy import db
from flaskblogmy.models import Post
from flaskblogmy.posts.forms import PostForm



posts = Blueprint('posts', __name__)


@posts.route('/post/new', methods=['GET', 'POST'])
@login_required # so that LoginManager would know this is accessible only if log on he needs to know where to login (set in __init__.py)
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title = form.title.data, content = form.content.data, author = current_user)
        db.session.add(post)
        db.session.commit()
        flash(f'Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title ='New Post', form = form, legend = 'New Post')

@posts.route('/post/<int:post_id>') # int is expected
def post(post_id): # post_id set in url_for when clicked on a link
    post = Post.query.get_or_404(post_id) # instead of get(),  gives 404 if doesnt exist
    return render_template('post.html', title=post.title, post=post)

@posts.route('/post/<int:post_id>/update', methods=['GET', 'POST']) # int is expected
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id) # instead of get() or filter_by(),  gives 404 if doesnt exist
    if post.author != current_user:
        abort(403) # http response for forbiden route
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit() # doesnt have to be .add, cos post.title/content are already in database
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title ='Update Post', form = form, legend = 'Update Post')


@posts.route('/post/<int:post_id>/delete', methods=['POST']) # int is expected
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id) # instead of get() or filter_by(),  gives 404 if doesnt exist
    if post.author != current_user:
        abort(403) # http response for forbidden route
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))


