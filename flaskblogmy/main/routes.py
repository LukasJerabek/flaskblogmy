
from flask import render_template, request, Blueprint
from flaskblogmy.models import Post


main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def home():
    # finds query url parameter
    page = request.args.get('page', 1, type=int) # we want page, default, type throws value arrow when anything different then int for page
    # without pagination - posts = Post.query.all()
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page,per_page=5) # always first page when not specifing
    return render_template('home.html', posts=posts)

# http://127.0.0.1:5000/?page=3 - accessing other pages through url

@main.route('/about')
def about():
    return render_template('about.html', title='About')

