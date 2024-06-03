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
    if msg.from_user.id == 6108693014 or 176163305:
        await msg.answer(f"Менюлардан бирини танланг", reply_markup=await main_menu())
        await state.set_state("main_menu")
    else:
        await msg.answer("Siz botdan foydalana olmaysiz\n"
                         "Botdan foydalanish uchun +998998787323 ga murojat qiling!")


@dp.message_handler(lambda message: message.text.startswith('get_user_id'))
async def get_user_id(message: types.Message):
    user = message.text.split()[1]
    print(user)
    chat = await bot.get_chat(user)
    print(chat)


@dp.message_handler(Text(add_group), state="main_menu")
async def add_group(msg: types.Message, state: FSMContext):
    await msg.answer("Гурух username ини киритинг‼ мисол учун:(@gurux_linki)‼")
    await state.set_state("group_link")


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
            await msg.answer("Gurux qoshildi botdan foydalanishingiz mumkin!", reply_markup=await main_menu())
            await state.set_state("main_menu")
        else:
            await msg.answer("Bu gurux allaqachon qoshilgan", reply_markup=await main_menu())
            await state.set_state("main_menu")
    except:
        await msg.answer("Гурух топилмади")
