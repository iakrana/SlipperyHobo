from apscheduler.schedulers.blocking import BlockingScheduler

import src.get_from_ladder
import src.spread_push

URL = "http://api.pathofexile.com/ladders/Slippery Hobo League (PL5357)"


def some_job():
    print('This job is run every 10 seconds.')


scheduler = BlockingScheduler()
scheduler.add_job(some_job, 'interval', seconds=10)
scheduler.start()
