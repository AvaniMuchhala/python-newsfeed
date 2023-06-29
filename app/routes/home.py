from flask import Blueprint, render_template, session, redirect
from app.models import Post
from app.db import get_db

bp = Blueprint('home', __name__, url_prefix='/')

# At /, render homepage with posts data
@bp.route('/')
def index():
  # Get all posts in descending order of creation time
  db = get_db()
  posts = db.query(Post).order_by(Post.created_at.desc()).all()
  return render_template('homepage.html', posts=posts, loggedIn=session.get('loggedIn'))

# At /login, render login or dashboard
@bp.route('/login')
def login():
  # Not logged in yet
  if session.get('loggedIn') is None:
    return render_template('login.html')
  return redirect('/dashboard')

# At /post/<id>, render single post with that ID
@bp.route('/post/<id>')
def single(id):
  # Get single post by id
  db = get_db()
  # filter = WHERE in mysql
  post = db.query(Post).filter(Post.id == id).one()

  # Render single post template
  return render_template(
    'single-post.html',
    post=post,
    loggedIn=session.get('loggedIn')
  )