from flask import Blueprint, request, jsonify
from app.models import User
from app.db import get_db

bp = Blueprint('api', __name__, url_prefix='/api')

# Post user info to /api/users
@bp.route('/users', methods=['POST'])
def signup():
  data = request.get_json()
  db = get_db()

  # Create new user  
  newUser = User(
    username = data['username'],
    email = data['email'],
    password = data['password']
  )

  # Save in database
  db.add(newUser) # prep INSERT statement
  db.commit() # update database

  return jsonify(id = newUser.id)