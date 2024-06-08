from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from bot.buttons.text import add_group, send_message, back_, messages
from db.models import Groups


async def main_menu():
    design = [
        [add_group, send_message]
    ]
    return ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True)


async def groups_button():
    design = []
    data = await Groups.get_all()
    for group_instance in data:
        group_id = group_instance[0].group_id
        username = group_instance[0].username
        if group_id and username:
            design.append([KeyboardButton(text=str(username + " " + group_id))])
    design.append([KeyboardButton(text=messages)])
    return ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True)


async def back():
    return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=back_)]], resize_keyboard=True)
