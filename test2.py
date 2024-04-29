# # import pandas as pd
# #
# #
# # def save_to_excel(data, file_name):
# #     df = pd.DataFrame(data, columns=["user_id", "username", "phone_number", "active"])
# #     df.to_excel(file_name, index=False)
# #
# #
# # data = [
# #     {"user_id": 3, "username": "user1", "phone_number": "123456789", "active": True},
# #     {"user_id": 4, "username": "user2", "phone_number": "987654321", "active": False},
# # ]
# #
# # file_name = "user_data.xlsx"
# # save_to_excel(data, file_name)
#
#
# from openpyxl import load_workbook, Workbook
# import os
#
# wb = Workbook(write_only=True)
# ws = wb.create_sheet()
#
#
# # def append_to_excel(new_data, file_name, sheet_name):
# #     wb = load_workbook(filename=file_name)
# #     ws = wb[sheet_name]
# #     for row in new_data:
# #         ws.append(row)
# #     wb.save(file_name)
# #
# #
# # file_name = 'example.xlsx'
# # sheet_name = 'Sheet1'
# #
# # append_to_excel(new_data, file_name, sheet_name)
#
#
# # result = [{
# #     'user_id': '1234565',
# #     'username': 'jamshid',
# #     'active': True
# # }]
# #
# #
# # ws.append(list(result[0].keys()))
# # for i in result:
# #     ws.append(list(i.values()))
# # wb.save('test.xlsx')
#
# def append_to_excel(result, file_name):
#     if not os.path.exists(file_name):
#         wb = Workbook()
#         ws = wb.active
#         ws.append(list(result[0].keys()))
#     else:
#         wb = load_workbook(filename=file_name)
#         ws = wb.active
#     for i in result:
#         ws.append(list(i.values()))
#     wb.save(file_name)
#
#
# result = [
#     {"Name": "Kedy", "Age": 50},
#     {"Name": "John", "Age": 14}
# ]
#
#
#
# file_name = 'test.xlsx'
# append_to_excel(result, file_name)


import asyncio
import datetime
import apscheduler.schedulers.asyncio as async_scheduler

from aiogram import Bot, Dispatcher, types

# Replace with your actual bot token
BOT_TOKEN = "6167118774:AAFRBd3pQonz2911YbUgRjTglKzGt2Ao__c"


async def send_scheduled_message(bot: Bot, group_id: int, message_id: int):
    await asyncio.sleep(1)
    try:
        await bot.send_message(chat_id=group_id, message_id=message_id)
        print(f"Sent scheduled message to group {group_id} (message ID: {message_id})")
    except Exception as e:
        print(f"Error sending message: {e}")


async def create_scheduled_task(bot: Bot, start_date: datetime.datetime, interval: int, group_id: int, message_id: int):
    scheduler = async_scheduler.AsyncScheduler()

    job = scheduler.add_job(
        send_scheduled_message, args=(bot, group_id, message_id), trigger="date", run_date=start_date
    )
    scheduler.start()

    # Schedule additional jobs based on interval
    while True:
        next_run_time = job.next_run_time
        if next_run_time:
            await asyncio.sleep((next_run_time - datetime.datetime.now()).total_seconds())
            job.reschedule(trigger="date", run_date=next_run_time)
        else:
            print(f"Scheduled task for group {group_id} has finished.")
            break

    await scheduler.shutdown()


async def main():
    # Initialize bot and dispatcher
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(bot)

    # Handle commands or events to create tasks dynamically (example)
    @dp.message_handler(commands=["schedule"])
    async def schedule_message(message: types.Message):
        # Extract parameters from message or user input
        start_date_str = message.text.split()[1]  # Replace with actual parsing logic
        interval = int(message.text.split()[2])  # Replace with actual parsing logic
        group_id = int(message.text.split()[3])  # Replace with actual parsing logic
        message_id = int(message.text.split()[4])  # Replace with actual parsing logic

        try:
            start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d %H:%M:%S")  # Adjust format as needed
        except ValueError:
            await message.reply("Invalid start date format. Please use YYYY-MM-DD HH:MM:SS.")
            return

        # Validate parameters (optional)

        await create_scheduled_task(bot, start_date, interval, group_id, message_id)
        await message.reply("Scheduled message creation successful!")

    # Start bot polling
    await dp.start_polling()


if __name__ == "__main__":
    asyncio.run(main())
