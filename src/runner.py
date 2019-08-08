from apscheduler.schedulers.blocking import BlockingScheduler
import time

import src.get_from_ladder
import src.spread_push


def some_job():
    global csv_string
    global index
    print('This job is run every hour.')
    # try:
    # ladder = src.get_from_ladder.all_chars_from_ladder(URL, dump=True)
    ladder = src.get_from_ladder.all_chars_from_ladder_csv(URL_CSV, dump=True)
    characters = src.get_from_ladder.all_items(ladder, dump=True)
    praise, shame, private, gone, other, rate_limit = src.get_from_ladder.split_into_lists(characters)
    gc, wks, exists = src.spread_push.worksheet("hobo_local_" + str(index) + "_" + time.strftime("%Y-%m-%d"))
    if exists:
        csv_string = src.spread_push.offending_items_string(shame, dump=True) + csv_string
    else:
        csv_string = src.spread_push.offending_items_string(shame, dump=True)
    src.spread_push.write_result_google_sheet(csv_string, private, gc, wks)
    if len(characters):
        print("Run number:          {:=2}\n"
              "Total characters:    {:=4}\n"
              "Praiseworthy:        {:=4}   {:=4}%\n"
              "Offenders:           {:=4}   {:=4}%\n"
              "Private:             {:=4}   {:=4}%\n"
              "Deleted:             {:=4}   {:=4}%\n"
              "Other error:         {:=4}   {:=4}%\n"
              "Rate Limited         {:=4}   {:=4}%".format(
                index,
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
    # except Exception as e:
    #     print("Exception")
    #     print(e)

if __name__ == "__main__":
    URL = "http://api.pathofexile.com/ladders/Slippery Hobo League (PL5357)"
    URL_testing = 'http://api.pathofexile.com/ladders/SSFHC RED LEAGUE (PL3306)'
    URL_CSV = 'https://www.pathofexile.com/ladder/export-csv/league/Slippery%20Hobo%20League%20(PL5357)?realm=pc'
    csv_string = ""
    index = 0
    print("started " + time.strftime("%Y-%m-%d %H:%M:%S"))

    scheduler = BlockingScheduler()
    scheduler.add_job(some_job, 'interval', hours=1,  start_date='2019-08-08 02:47:20')
    # scheduler.add_job(some_job, 'interval', minutes=1)
    scheduler.start()
