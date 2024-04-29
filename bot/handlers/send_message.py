from datetime import datetime, timedelta
from asyncio import get_event_loop

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ContentType, ReplyKeyboardRemove
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.buttons.reply_button import groups_button, main_menu, back
from bot.buttons.text import send_message, back_
from bot.dispatcher import dp, bot
from db.models import Groups, Messages

scheduler = AsyncIOScheduler()


async def create_task_func(chat_id, message_id, from_chat_id):
    await bot.forward_message(chat_id=chat_id, message_id=message_id, from_chat_id=from_chat_id)


def schedule_forwarding(chat_id, message_id, from_chat_id, days_, hours_, minutes_):
    scheduler.add_job(create_task_func, 'interval', hours=hours_, minutes=minutes_,
                      args=(chat_id, message_id, from_chat_id),
                      end_date=datetime.now() + timedelta(days=days_))
    scheduler.start()


@dp.message_handler(Text(send_message), state="*")
async def send_message(msg: types.Message, state: FSMContext):
    await state.set_state("choosen_group")
    await msg.answer("Habar yubormoqchi bolgan chatni tanlang!!", reply_markup=await groups_button())
    data = await Groups.get_all()


@dp.message_handler(state="choosen_group")
async def send_message_to_group(msg: types.Message, state: FSMContext):
    group_id = "-"
    data = str(msg.text)
    group_id += data.split("-")[1]
    async with state.proxy() as data:
        data['group_id'] = group_id
    await msg.answer("Yubormoqchi bolgan habaringizni kiriting", reply_markup=ReplyKeyboardRemove())
    await state.set_state("message")


@dp.message_handler(content_types=ContentType.PHOTO, state="message")
async def send_photo_to_group(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['message_id'] = msg.message_id
    await msg.answer("Yuborish vaqtini kiriting[Kun-Soat-Minut = 30-1-30]\n"
                     "Agar soat yoki minutni kirgizishni istamasangiz 0 kiritib keting",
                     reply_markup=await back()
                     )
    await state.set_state('schedule')


@dp.message_handler(content_types=ContentType.VIDEO, state="message")
async def send_video_to_group(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['message_id'] = msg.message_id
    await msg.answer("Yuborish vaqtini kiriting[Kun-Soat-Minut = 30-1-30]\n"
                     "Agar soat yoki minutni kirgizishni istamasangiz 0 kiritib keting",
                     reply_markup=await back())
    await state.set_state('schedule')


@dp.message_handler(content_types=ContentType.ANY, state="message")
async def send_message_handler(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['message_id'] = msg.message_id
    await msg.answer("Yuborish vaqtini kiriting[Kun-Soat-Minut = 30-1-30]\n"
                     "Agar soat yoki minutni kirgizishni istamasangiz 0 kiritib keting",
                     reply_markup=await back())
    await state.set_state('schedule')


@dp.message_handler(state="schedule")
async def save_time_date(msg: types.Message, state: FSMContext):
    try:
        a, b, c = msg.text.split("-")
        print(a, b, c)
        print(msg.text)
        async with state.proxy() as data:
            print(data)
            group_id = data.get('group_id')
            message_id = data.get("message_id")
        print(data)
        schedule_forwarding(chat_id=group_id, message_id=message_id, from_chat_id=msg.from_user.id, days_=int(a),
                            hours_=int(b),
                            minutes_=int(c))
        await msg.answer("Yuborish boshlandi", reply_markup=await main_menu())
        await state.set_state("main_menu")
    except:
        await msg.answer("Yuborish boshlandi damingizni olishingiz mumkin!")
