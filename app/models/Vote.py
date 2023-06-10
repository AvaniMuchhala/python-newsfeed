from app.db import Base
from sqlalchemy import Column, Integer, ForeignKey

class Vote(Base):
  __tablename__ = 'votes'
  id = Column(Integer, primary_key=True)
  # User who upvoted post
  user_id = Column(Integer, ForeignKey('users.id'))
  # Post being upvoted
  post_id = Column(Integer, ForeignKey('posts.id'))