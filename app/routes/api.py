import sys
from flask import Blueprint, request, jsonify
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

  return jsonify(id = newUser.id)