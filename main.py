import asyncio
import logging
from asyncio import get_event_loop

from aiogram import executor
from bot.dispatcher import dp, bot
import bot.handlers
from db import db
from db.models import Users, Groups, Messages
from apscheduler.schedulers.asyncio import AsyncIOScheduler

logging.basicConfig(level=logging.INFO)
scheduler = AsyncIOScheduler()

# async def create_all():
#     await db.create_all()
#     await Users().create()
#     await Groups().create()
#     await Messages().create()

if __name__ == '__main__':
    db.init()
    scheduler.start()
    executor.start_polling(dp, skip_updates=True)
    loop = get_event_loop()
    # loop.run_until_complete(create_all())
    logging.getLogger('apscheduler').setLevel(logging.DEBUG)
    loop.run_forever()
