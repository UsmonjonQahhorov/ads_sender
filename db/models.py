from datetime import datetime

from sqlalchemy import Column, String, Sequence, Boolean, Integer, Float, DateTime, ForeignKey
from db import db
from db.utils import CreatedModel

db.init()


class Users(CreatedModel):
    __tablename__ = 'users'
    id = Column(Integer, Sequence("user_id_seq"), primary_key=True)
    user_id = Column(String())
    username = Column(String(255))


class Groups(CreatedModel):
    __tablename__ = 'groups'
    id = Column(Integer, Sequence('group_id_seq'), primary_key=True)
    group_id = Column(String())
    username = Column(String())


class Messages(CreatedModel):
    __tablename__ = "messages"
    id = Column(Integer, Sequence('message_id_seq'), primary_key=True)
    message_id = Column(Integer)
    schedule = Column(String())
    group_id = Column(Integer, ForeignKey("groups.id"))
