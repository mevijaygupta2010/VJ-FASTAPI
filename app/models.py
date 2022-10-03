from enum import unique
from psycopg2 import Timestamp
from .database import Base
from sqlalchemy.sql.expression import text
from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, Integer,String
from sqlalchemy.orm import relationship

class Post(Base):
    __tablename__ ="posts"
    id =Column(Integer, primary_key=True, nullable=False)
    owner_id=Column(Integer,ForeignKey("users.id",ondelete="CASCADE",onupdate="CASCADE"),nullable=False)
    title =Column(String, nullable=False)
    content =Column(String,  nullable=False)
    published =Column(Boolean, server_default='True', nullable=False)
    created_at =Column(TIMESTAMP(timezone= True),nullable=False,server_default=text('now()'))

    owner= relationship("User")

class User(Base):
    __tablename__="users"
    id =Column(Integer, primary_key=True, nullable=False)
    email = Column(String,nullable=False,unique=True)
    password= Column(String,nullable=False)
    created_at =Column(TIMESTAMP(timezone= True),nullable=False,server_default=text('now()'))
    phone_number=Column(String)

class Vote(Base):
    __tablename__ ="votes"
    user_id=Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),primary_key=True)
    post_id=Column(Integer,ForeignKey("posts.id",ondelete="CASCADE"),primary_key=True)
    

