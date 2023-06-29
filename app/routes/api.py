import sys
from flask import Blueprint, request, jsonify, session
from app.models import User, Post, Comment, Vote
from app.db import get_db
from app.utils.auth import login_required

bp = Blueprint('api', __name__, url_prefix='/api')

# Post user info to /api/users
@bp.route('/users', methods=['POST'])
def signup():
  data = request.get_json()
  db = get_db()

  try:
    # Attempt creating a new user  
    newUser = User(
      username = data['username'],
      email = data['email'],
      password = data['password']
    )

    # Save in database
    db.add(newUser) # prep INSERT statement
    db.commit() # update database
  except:
    print(sys.exc_info()[0])
    
    # Insert failed, so rollback last pending commit and send JSON error to front end
    # Set response status code to 500 to indicate that a server error occurred
    db.rollback()
    return jsonify(message = 'Signup failed'), 500

  # Clears any existing session data and creates new session properties
  session.clear()
  session['user_id'] = newUser.id
  session['loggedIn'] = True
  return jsonify(id = newUser.id)

@bp.route('/users/login', methods=['POST'])
def login():
  data = request.get_json()
  db = get_db()

  # Check whether user's email address exists in DB
  try:
    user = db.query(User).filter(User.email == data['email']).one()
  except:
    print(sys.exc_info()[0])
    return jsonify(message = 'Incorrect credentials'), 400
  
  # If user found with same inputted email address, verify password
  if user.verify_password(data['password']) == False:
    return jsonify(message = 'Incorrect credentials'), 400
  
  session.clear()
  session['user_id'] = user.id
  session['loggedIn'] = True

  return jsonify(id = user.id)

@bp.route('/users/logout', methods=['POST'])
def logout():
  # Remove session variables
  session.clear()
  return '', 204

@bp.route('/posts', methods=['POST'])
@login_required
def create():
  data = request.get_json()
  db = get_db()

  try:
    # Create a new post
    newPost = Post(
      title = data['title'],
      post_url = data['post_url'],
      user_id = session.get('user_id')
    )

    db.add(newPost)
    db.commit()
  except:
    print(sys.exc_info()[0])

    db.rollback()
    return jsonify(message = 'Post failed'), 500

  return jsonify(id = newPost.id)

@bp.route('/posts/<id>', methods=['PUT'])
@login_required
def update(id):
  data = request.get_json()
  db = get_db()

  try:
    # Retrieve post and update title property
    post = db.query(Post).filter(Post.id == id).one()
    post.title = data['title']
    db.commit()
  except:
    print(sys.exc_info()[0])

    db.rollback()
    return jsonify(message = 'Post not found'), 404
  
  return '', 204

@bp.route('/posts/<id>', methods=['DELETE'])
@login_required
def delete(id):
  db = get_db()

  try:
    # Delete post from db
    db.delete(db.query(Post).filter(Post.id == id).one())
    db.commit()
  except:
    print(sys.exc_info()[0])

    db.rollback()
    return jsonify(message = 'Post not found'), 404

  return '', 204

@bp.route('/posts/upvote', methods=['PUT'])
@login_required
def upvote():
  data = request.get_json()
  db = get_db()

  try:
    # Create a new vote with incoming id and session id
    newVote = Vote(
      post_id = data['post_id'],
      user_id = session.get('user_id')
    )

    db.add(newVote)
    db.commit()
  except:
    print(sys.exc_info()[0])

    db.rollback()
    return jsonify(message = 'Upvote failed'), 500

  return '', 204

@bp.route('/comments', methods=['POST'])
@login_required
def comment():
  data = request.get_json()
  db = get_db()

  try:
    # Create a new comment
    newComment = Comment(
      comment_text = data['comment_text'],
      post_id = data['post_id'],
      user_id = session.get('user_id')
    )

    db.add(newComment)
    db.commit()
  except:
    print(sys.exc_info()[0])
    
    db.rollback()
    return jsonify(message = 'Comment failed'), 500
  
  return jsonify(id = newComment.id)