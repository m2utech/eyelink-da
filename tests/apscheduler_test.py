from apscheduler.schedulers.blocking import BlockingScheduler


def job_function():
     print ("Hello World")

sched = BlockingScheduler()

# Schedules job_function to be run on the third Friday
# of June, July, August, November and December at 00:00, 01:00, 02:00 and 03:00
sched.add_job(job_function, 'cron', day_of_week='mon-fri', second='*/3')

sched.start()