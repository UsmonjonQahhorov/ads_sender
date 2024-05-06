import json
import requests
import aiofiles
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart, Text
from aiogram import types

from db.models import Users, Groups
from db.utils import AbstractClass
from bot.buttons.reply_button import main_menu, groups_button
from bot.buttons.text import add_group, send_message
from bot.dispatcher import dp, bot


@dp.message_handler(CommandStart(), state='*')
async def start_handler(msg: types.Message, state: FSMContext):
    await msg.answer(f"Менюлардан бирини танланг", reply_markup=await main_menu())
    await state.set_state("main_menu")


@dp.message_handler(Text(add_group), state="main_menu")
async def add_group(msg: types.Message, state: FSMContext):
    await msg.answer("Гурух username ини киритинг‼ мисол учун:(@gurux_linki)‼")
    await state.set_state("group_link")


# @dp.message_handler(Text(send_message), state="main_menu")
# async def send_message(msg: types.Message, state: FSMContext):
#     await state.set_state("choosen_group")
#     await msg.answer("Habar yubormoqchi bolgan chatni tanlang!!", reply_markup=await groups_button())
#     data = await Groups.get_all()


@dp.message_handler(state="group_link")
async def save_group(msg: types.Message, state: FSMContext):
    try:
        group_link = msg.text
        group = group_link
        chat = await bot.get_chat(group)
        username = chat['username']
        group_id = chat['id']
        user = await Groups.get_by_chat_id(chat_id=group_id)
        if user is None:
            await Groups.create(group_id=str(group_id), username=str(username))
        else:
            await msg.answer("Bu gurux allaqachon qoshilgan")
    except:
        await msg.answer("Гурух топилмади")
