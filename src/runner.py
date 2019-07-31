from apscheduler.schedulers.blocking import BlockingScheduler

import src.get
import src.spread_it_for_me




url = "http://api.pathofexile.com/ladders/Slippery Hobo League (PL5357)"

ladder_output = src.get.all_chars_from_ladder(url, dump=True)

characters = src.get.all_items(ladder_output, dump=True)

praise, shame, private, gone, other, rate_limit = src.get.split_into_lists(characters)

csv_string = src.spread_it_for_me.offending_items_string(shame)


sched = BlockingScheduler()

@sched.scheduled_job('interval', seconds=10)
def timed_job():
    print('This job is run every 10 seconds.')

@sched.scheduled_job('cron', day_of_week='mon-fri', hour=10)
def scheduled_job():
    print('This job is run every weekday at 10am.')

sched.configure(options_from_ini_file)
sched.start()