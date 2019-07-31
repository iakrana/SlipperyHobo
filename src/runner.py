from apscheduler.schedulers.blocking import BlockingScheduler

import src.get
# import src.spread_it_for_me




def some_job():
    print('This job is run every 10 seconds.')

scheduler = BlockingScheduler()
scheduler.add_job(some_job, 'interval', seconds=10)
scheduler.start()