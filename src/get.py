import json
import time
import requests
import gzip
from timeit import default_timer as timer

# TODO compression of json objects
import gzip
from io import StringIO, BytesIO


def get_all_chars(URL, dump=False):
    def get_total_and_time():
        params = {'offset': 0, 'limit': 1}
        # TODO: Be nice and do some fallback stuff
        r = requests.get(url=URL, params=params)
        data = r.json()
        return data['total'], data['cached_since']

    def get_chars(offset_, limit_):
        params = {'offset': offset_, 'limit': limit_}
        time.sleep(1.5)
        # TODO: Be nice and do some fallback stuff
        r = requests.get(url=URL, params=params)
        data = r.json()
        return data['entries']

    total, time_cached = get_total_and_time()
    total_left = total
    all_chars = []
    print("Total:", total)
    while total_left > 0:
        offset = total - total_left
        if total_left > 200:
            limit = 200
        else:
            limit = total_left
        all_chars.extend(get_chars(offset, limit))
        total_left = total_left - limit
        print("# left:", total_left)
    print("Done")
    if dump:
        fname = "../data/ladder_" + time.strftime("%Y%m%d-%H%M%S") + '.json.gz'
        print("Dumping to file: " + fname)
        with gzip.GzipFile(fname, 'w') as fout:
            fout.write(json.dumps(all_chars).encode('utf-8'))
    return time_cached, all_chars


# Slow as molasses
def get_all_items(all_chars, dump=False):
    rate_limiter = 1.5
    account_item = [{'accountName': entry['account']['name'], 'character': entry['character']['name']}
                    for entry in all_chars if 'retired' not in entry.keys()]
    URL_get_items = 'https://www.pathofexile.com/character-window/get-items'
    start_get = timer()
    for i, param in enumerate(account_item):
        print(i, param)
        start = timer()
        # TODO: Be nice and do some fallback stuff
        param['inventory'] = requests.get(url=URL_get_items, params=param).json()
        end = timer()
        time.sleep(rate_limiter - (end-start))
        if 'error' in param['inventory']:
            print(param['inventory']['error'])
    if dump:
        fname = "../data/items_" + time.strftime("%Y%m%d-%H%M%S") + '.json.gz'
        print("Dumping to file: " + fname)
        with gzip.GzipFile(fname, 'w') as fout:
            fout.write(json.dumps(account_item).encode('utf-8'))
    end_get = timer()
    print("Time spent getting", end_get - start_get)
    return account_item


def split_lists_of_bad(char_account_items):
    gone_ = []
    rate_limit_ = []
    private_ = []
    other_ = []
    shame_ = []
    praise_ = []
    for char in char_account_items:
        if 'error' in char['inventory']:
            if char['inventory']['error']['code'] == 1:
                gone_.append(char['accountName'])
            elif char['inventory']['error']['code'] == 2:
                other_.append(char)
            elif char['inventory']['error']['code'] == 3:
                rate_limit_.append(char['accountName'])
            elif char['inventory']['error']['code'] == 4:
                other_.append(char)
            elif char['inventory']['error']['code'] == 5:
                other_.append(char)
            elif char['inventory']['error']['code'] == 6:
                private_.append(char['accountName'])
            else:
                print("?", char)
        else:
            bad = False
            for item in char['inventory']['items']:
                if item['frameType'] != 3 and item['inventoryId'] != 'Flask':
                    bad = True
            if bad:
                shame_.append(char)
            else:
                praise_.append(char)
    return praise_, shame_, private_, gone_, other_, rate_limit_


def percent_of_tot(partial, tot):
    return round(len(partial) / len(tot) * 100, 2)


if __name__ == "__main__":
    URL_tarke = "http://api.pathofexile.com/ladders/OneFreeSubEachAndEveryMonthBTW (PL4673)"
    time_cache, all_chars = get_all_chars(URL_tarke, dump=False)
    all_items = get_all_items(all_chars, dump=True)
    praise, shame, private, gone, other, rate_limit = split_lists_of_bad(all_items)

    print("League: OneFreeSubEachAndEveryMonthBTW%20(PL4673)")
    print("Total characters                     :", len(all_items))
    print("Praiseworthy(Probably naked)         :", len(praise), "   ,", percent_of_tot(praise, all_items), "%", )
    print("Shameful                             :", len(shame), "  ,", percent_of_tot(shame, all_items), "%")
    print("Private                              :", len(private), "   ,", percent_of_tot(private, all_items), "%")
    print("Gone                                 :", len(gone), "  ,", percent_of_tot(gone, all_items), "%")
    print("Rate Limited because I was ddosing   :", len(rate_limit), "  ,", percent_of_tot(rate_limit, all_items), "%")


    # Read result all_char
    # with open('data.json') as json_file:
    #     data = json.load(json_file)

    # # Read result all_items
    # with open('../test_data/char_item.json') as json_file:
    #     item_data = json.load(json_file)
