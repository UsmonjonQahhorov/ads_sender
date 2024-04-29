import datetime
import os

import pytz
from dotenv import load_dotenv
from sqlalchemy.future import select

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

from sqlalchemy import text, Column, DateTime
from db import db, Base

db.init()


class AbstractClass:
    @staticmethod
    async def commit():
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise

    @classmethod
    async def insert_into(cls, database, column, value):
        query = text(f"INSERT INTO {database} ({column}) VALUES (:column_value)")
        await db.execute(query, {'column_value': value})
        await db.commit()

    @classmethod
    async def create(cls, **kwargs):
        object_ = cls(**kwargs)
        db.add(object_)
        await cls.commit()
        return object_

    async def get_by_id(cls, id):
        chat_id_str = str(id)
        query = select(cls).where(cls.user_id == chat_id_str)
        objects = await db.execute(query)
        object_ = objects.first()
        return object_

    @classmethod
    async def get_all(cls):
        query = select(cls)
        objects = await db.execute(query)
        return objects.all()

    @classmethod
    async def get_by_chat_id(cls, chat_id: str):
        chat_id_str = str(chat_id)
        query = select(cls).where(cls.group_id == chat_id_str)
        objects = await db.execute(query)
        object_ = objects.first()
        return object_


class CreatedModel(Base, AbstractClass):
    __abstract__ = True
    tz = pytz.timezone('Asia/Tashkent')

    created_at = Column(DateTime(timezone=True), default=datetime.datetime.now(tz), server_default="now()")
    updated_at = Column(DateTime(timezone=True), default=datetime.datetime.now(tz), onupdate=datetime.datetime.now(tz),
                        server_default="now()")
