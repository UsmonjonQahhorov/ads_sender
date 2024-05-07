from datetime import datetime, timedelta
from asyncio import get_event_loop
from uuid import uuid4

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ContentType, ReplyKeyboardRemove
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.buttons.reply_button import groups_button, main_menu, back
from bot.buttons.text import send_message, back_, messages
from bot.dispatcher import dp, bot
from db.models import Groups, Messages

scheduler = AsyncIOScheduler()

list_ = []


async def create_task_func(chat_id, message_id, from_chat_id):
    await bot.forward_message(chat_id=chat_id, message_id=message_id, from_chat_id=from_chat_id)


def schedule_forwarding(chat_id, message_id, from_chat_id, days_, hours_, minutes_):
    # scheduler.start()
    job_id = str(uuid4())
    print(f"Adding job with ID: {job_id}, message_id: {message_id}, group_id: {chat_id}")
    scheduler.add_job(create_task_func, 'interval', hours=hours_, minutes=minutes_, id=job_id,
                      args=(chat_id, message_id, from_chat_id),
                      end_date=datetime.now() + timedelta(days=days_))


@dp.message_handler(Text(send_message), state="*")
async def send_message(msg: types.Message, state: FSMContext):
    await state.set_state("choosen_group")
    await msg.answer("Habar yubormoqchi bolgan chatlarni tanlang!!", reply_markup=await groups_button())


@dp.message_handler(state="choosen_group")
async def send_message(msg: types.Message, state: FSMContext):
    if msg.text == messages:
        await send_message_to_group(msg, state)
    else:
        await msg.answer("Tanlang", reply_markup=await groups_button())
        list_.append(msg.text)
        async with state.proxy() as data:
            data["groups_id_"] = list_
        await state.set_state("choosen_group")


@dp.message_handler(Text([messages]), state="choosen_group")
async def send_message_to_group(msg: types.Message, state: FSMContext):
    await msg.answer("Yubormoqchi bolgan habaringizni kiriting", reply_markup=ReplyKeyboardRemove())
    await state.set_state("message")


@dp.message_handler(content_types=ContentType.PHOTO, state="message")
async def send_photo_to_group(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['message_id'] = msg.message_id
    await msg.answer("Yuborish vaqtini kiriting[Kun-Soat-Minut = 30-1-30]\n"
                     "Agar soat yoki minutni kiritishni istamasangiz 0 kiritib keting",
                     reply_markup=await back()
                     )
    await state.set_state('schedule')


@dp.message_handler(content_types=ContentType.VIDEO, state="message")
async def send_video_to_group(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['message_id'] = msg.message_id
    await msg.answer("Yuborish vaqtini kiriting[Kun-Soat-Minut = 30-1-30]\n"
                     "Agar soat yoki minutni kiritishni istamasangiz 0 kiritib keting",
                     reply_markup=await back())
    await state.set_state('schedule')


@dp.message_handler(content_types=ContentType.ANY, state="message")
async def send_message_handler(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['message_id'] = msg.message_id
    await msg.answer("Yuborish vaqtini kiriting[Kun-Soat-Minut = 30-1-30]\n"
                     "Agar soat yoki minutni kiritishni istamasangiz 0 kiritib keting",
                     reply_markup=await back())
    await state.set_state('schedule')


@dp.message_handler(state="schedule")
async def save_time_date(msg: types.Message, state: FSMContext):
    try:
        a, b, c = map(int, msg.text.split("-"))
        async with state.proxy() as data:
            message_id = data.get("message_id")
            groups_ = data["groups_id_"]
            for group_info in groups_:
                group_id = group_info.split(" ")[1]
                print(group_id)
                schedule_forwarding(chat_id=group_id,
                                    message_id=message_id,
                                    from_chat_id=msg.from_user.id,
                                    days_=a, hours_=b, minutes_=c)
        scheduler.start()
        await msg.answer("Yuborish boshlanmadi. Damingizni olishingiz mumkin!", reply_markup=await main_menu())
        await state.set_state("main_menu")

    except Exception as e:
        print(f"An error occurred: {e}")
        await msg.answer("Yuborish boshlanmadi. Damingizni olishingiz mumkin!")
