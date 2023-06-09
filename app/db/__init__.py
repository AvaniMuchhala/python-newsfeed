from os import getenv
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
# g object can be shared across modules as long as context is still active
from flask import g

load_dotenv()

# connect to database using env variable
engine = create_engine(getenv('DB_URL'), echo=True, pool_size=20, max_overflow=0)
Session = sessionmaker(bind=engine)
Base = declarative_base()

def init_db(app):
  Base.metadata.create_all(engine)
  
  app.teardown_appcontext(close_db)

# Saves current connection on g object if not already there. Returns session-connection
def get_db():
  if 'db' not in g:
    # Store db connection in app context
    g.db = Session()

  return g.db

# Close connection
def close_db(e=None):
  # Find and remove db from g object 
  db = g.pop('db', None)

  if db is not None:
    db.close()