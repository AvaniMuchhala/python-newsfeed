from datetime import datetime
from app.db import Base
from .Vote import Vote
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, select, func
from sqlalchemy.orm import relationship, column_property

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    post_url = Column(String(100), nullable=False)
    # References users table
    user_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    user = relationship('User')
    # Deleting post from DB deletes all its comments and votes
    comments = relationship('Comment', cascade='all,delete')
    votes = relationship('Vote', cascade='all,delete')

    # Dynamic property to add up votes associated to this post
    vote_count = column_property(
        select([func.count(Vote.id)]).where(Vote.post_id == id)
    )
