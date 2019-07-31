from apscheduler.schedulers.blocking import BlockingScheduler
import time

import src.get_from_ladder
import src.spread_push

URL = "http://api.pathofexile.com/ladders/Slippery Hobo League (PL5357)"

csv_string = []


def some_job():
    global csv_string
    print('This job is run every hour.')
    ladder = src.get_from_ladder.all_chars(URL, dump=True)
    characters = src.get_from_ladder.all_items(ladder, dump=True)
    praise, shame, private, gone, other, rate_limit = src.get_from_ladder.split_into_lists(characters)
    gc, wks, exists = src.spread_push.worksheet(time.strftime("%Y-%m-%d"))
    if exists:
        csv_string = src.spread_push.offending_items_string(shame, dump=True) + csv_string
    else:
        csv_string = src.spread_push.offending_items_string(shame, dump=True)
    src.spread_push.write_result_google_sheet(csv_string, private, gc, wks)


scheduler = BlockingScheduler()
scheduler.add_job(some_job, 'interval', hours=1)
scheduler.start()
