from apscheduler.schedulers.blocking import BlockingScheduler
import time

import src.get_from_ladder
import src.spread_push

URL = "http://api.pathofexile.com/ladders/Slippery Hobo League (PL5357)"
URL_testing = 'http://api.pathofexile.com/ladders/SSFHC RED LEAGUE (PL3306)'
csv_string = ""
index = 0
print("started " + time.strftime("%Y-%m-%d %H:%M:%S"))


def some_job():
    global csv_string
    global index
    print('This job is run every hour.')
    # org: ladder = src.get_from_ladder.all_chars(URL, dump=True)
    ladder = src.get_from_ladder.all_chars_from_ladder(URL_testing, dump=True)
    characters = src.get_from_ladder.all_items(ladder, dump=True)
    praise, shame, private, gone, other, rate_limit = src.get_from_ladder.split_into_lists(characters)
    # testing
    gc, wks, exists = src.spread_push.worksheet("hobo_" + index + "_" + time.strftime("%Y-%m-%d-%H"))
    # org: gc, wks, exists = src.spread_push.worksheet(time.strftime("%Y-%m-%d"))
    if exists:
        csv_string = src.spread_push.offending_items_string(shame, dump=True) + csv_string
    else:
        csv_string = src.spread_push.offending_items_string(shame, dump=True)
    src.spread_push.write_result_google_sheet(csv_string, private, gc, wks)
    if len(characters):
        print("Total characters:    {:=4}%\n"
              "Praiseworthy:        {:=4} {:=4}%\n"
              "Offenders:           {:=4} {:=4}%\n"
              "Private:             {:=4} {:=4}%\n"
              "Deleted:             {:=4} {:=4}%\n"
              "Other error:         {:=4} {:=4}%\n"
              "Rate Limited         {:=4} {:=4}%".format(
                len(characters),
                len(praise), src.get_from_ladder.percent_of_tot(praise, characters),
                len(shame), src.get_from_ladder.percent_of_tot(shame, characters),
                len(private), src.get_from_ladder.percent_of_tot(private, characters),
                len(gone), src.get_from_ladder.percent_of_tot(gone, characters),
                len(other), src.get_from_ladder.percent_of_tot(other, characters),
                len(rate_limit), src.get_from_ladder.percent_of_tot(rate_limit, characters),
                )
              )
    else:
        print("Empty League")


scheduler = BlockingScheduler()
# org: scheduler.add_job(some_job, 'interval', hours=1)
scheduler.add_job(some_job, 'interval', minutes=15,  start_date='2019-07-31 18:49:00')
scheduler.start()
