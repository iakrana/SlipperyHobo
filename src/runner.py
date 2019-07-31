from apscheduler.schedulers.blocking import BlockingScheduler
import time

import src.get_from_ladder
import src.spread_push

URL = "http://api.pathofexile.com/ladders/Slippery Hobo League (PL5357)"


def some_job():
    print('This job is run every hour.')
    ladder = src.get_from_ladder.all_chars(URL)
    characters = src.get_from_ladder.all_items(ladder)
    praise, shame, private, gone, other, rate_limit = src.get_from_ladder.split_into_lists(characters)
    csv_string = src.spread_push.offending_items_string(shame, True)
    src.spread_push.write_result_google_sheet(csv_string, private, time.strftime("%Y-%m-%d"))


scheduler = BlockingScheduler()
scheduler.add_job(some_job, 'interval', hours=1)
scheduler.start()
