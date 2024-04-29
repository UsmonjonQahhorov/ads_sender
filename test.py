# from datetime import datetime, timedelta
#
# from apscheduler.schedulers.background import BlockingScheduler
#
#
# def display(message_id):
#     print(f"This is the display function {message_id} !!!")
#
#
# def create_tasks(intervals, message_id):
#     schedulers = []
#     for interval in intervals:
#         scheduler = BlockingScheduler()
#         job_id = scheduler.add_job(display, 'interval', seconds=interval, args=[message_id],
#                                    end_date=datetime.now() + timedelta(days=7))
#         schedulers.append((scheduler, job_id))
#         scheduler.start()
#
#         # Print details of each job
#         jobs = scheduler.get_jobs()
#         for job in jobs:
#             print("Job Args:", job.args)
#             print("Job Name:", job.name)
#             print("Job ID:", job.id)
#             print("Job Next Run Time:", job.next_run_time)
#
#     return schedulers
#
#
# intervals = [5, 10, 15]
#
# schedulers = create_tasks(intervals, message_id=1)
