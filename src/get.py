import json
import time
import requests


def get_all_chars():
    URL_get_ladder = "http://api.pathofexile.com/ladders/OneFreeSubEachAndEveryMonthBTW%20(PL4673)"

    def get_total_and_time():
        params = {'offset': 0, 'limit': 1}
        r = requests.get(url=URL_get_ladder, params=params)
        data = r.json()
        return data['total'], data['cached_since']

    def get_chars(offset_, limit_):
        params = {'offset': offset_, 'limit': limit_}
        time.sleep(1.5)
        r = requests.get(url=URL_get_ladder, params=params)
        data = r.json()
        return data['entries']

    total, time_cached = get_total_and_time()
    total_left = total
    all_chars = []
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
    return [time_cached, all_chars]


# Slow as molasses
def get_all_items(all_chars):
    account_item = [{'accountName': entry['account']['name'], 'character': entry['character']['name']}
                     for entry in all_chars]
    URL_get_items = 'https://www.pathofexile.com/character-window/get-items'
    for param in account_item:
        print(param)
        time.sleep(1.5)
        param['inventory'] = requests.get(url=URL_get_items, params=param).json()
        print(param['inventory'])
    return account_item


def split_lists_of_bad(item_data):
    gone = []
    rate_limit = []
    rate_limit = []
    private = []
    other = []
    shame = []
    praise = []
    for char in item_data:
        if 'error' in char['inventory']:
            if char['inventory']['error']['code'] == 1:
                gone.append(char['accountName'])
            elif char['inventory']['error']['code'] == 2:
                other.append(char)
            elif char['inventory']['error']['code'] == 3:
                rate_limit.append(char['accountName'])
            elif char['inventory']['error']['code'] == 4:
                other.append(char)
            elif char['inventory']['error']['code'] == 5:
                other.append(char)
            elif char['inventory']['error']['code'] == 6:
                private.append(char['accountName'])
            else:
                print("?", char)
        else:
            bad = False
            for item in char['inventory']['items']:
                if item['frameType'] != 3:
                    bad = True
            if bad:
                shame.append(char)
            else:
                praise.append(char)
    return praise, shame, private, gone, other, rate_limit


def percent_of_tot(partial):
    return round(len(partial) / len(item_data) * 100, 2)


if __name__ == "__main__":
    # # Write result all_chars
    # with open('data.json', 'w') as outfile:
    #     json.dump(get_all_chars()[1], outfile)

    # Read result all_char
    # with open('data.json') as json_file:
    #     data = json.load(json_file)

    # Write result all_items
    # with open('param_item.json', 'w') as outfile:
    #     json.dump(get_all_items(data), outfile)

    # # Read result all_items
    with open('../test_data/char_item.json') as json_file:
        item_data = json.load(json_file)

    praise, shame, private, gone, other, rate_limit = split_lists_of_bad(item_data)
    print("League: OneFreeSubEachAndEveryMonthBTW%20(PL4673)")
    print("Total characters                     :", len(item_data))
    print("Praiseworthy(Probably naked)         :", len(praise), "   ,",  percent_of_tot(praise), "%", )
    print("Shameful                             :", len(shame),  "  ,", percent_of_tot(shame), "%")
    print("Private                              :", len(private),"   ,", percent_of_tot(private), "%")
    print("Gone                                 :", len(gone),   "  ,", percent_of_tot(gone), "%")
    print("Rate Limited because I was ddosing   :", len(rate_limit), "  ,", percent_of_tot(rate_limit), "%")
