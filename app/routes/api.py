import sys
from flask import Blueprint, request, jsonify, session
from app.models import User
from app.db import get_db

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