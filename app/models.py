from app.database import Base
from sqlalchemy import Column,Integer,String,Boolean,DateTime
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from datetime import datetime

class PostModel(Base):
    __tablename__ = "posts"
    
    Id = Column(Integer, primary_key=True, nullable=False)
    Name = Column(String,nullable=False)
    Domain = Column(String)
    Age = Column(Integer,nullable=False)
    Email = Column(String)
    Is_student = Column(Boolean,server_default='True')
    Rating = Column(Integer,server_default='3')
    Created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))

class User(Base):
    __tablename__ = "users"
    
    Id = Column(Integer, primary_key=True, nullable=False)
    Email = Column(String,nullable=False,unique=True)
    Password = Column(String,nullable=False)
    Created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))



class ActiveSession(Base):
    __tablename__ = "active_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)  # Reference to the User ID
    token = Column(String, unique=True, index=True)  # Store the token (optional but can be useful for invalidation)
    created_at = Column(DateTime, default=datetime.utcnow)  # When the session was created
    expires_at = Column(DateTime)  # When the token will expire