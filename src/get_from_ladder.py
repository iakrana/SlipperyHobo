#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Getters for characters, items and passive tree jewels for a league.
Uses ladder, character and passive api from GGG
"""

import gzip
import json
import time
import datetime
from timeit import default_timer as timer

import requests


def all_chars_from_ladder(url, dump=False):
    def get_total_and_time():
        params = {'offset': 0, 'limit': 1}
        # TODO: Be nice and do some fallback stuff
        r = requests.get(url=url, params=params)
        data_ = r.json()
        if 'cached_since' in data_:
            return data_['total'], data_['cached_since']
        else:
            return data_['total'], None

    def get_chars(offset_, limit_):
        params = {'offset': offset_, 'limit': limit_}
        time.sleep(1.5)
        # TODO: Be nice and do some fallback stuff
        r = requests.get(url=url, params=params)
        data_ = r.json()
        return data_['entries']

    total, time_cached = get_total_and_time()
    total_left = total
    all_chars_ = []
    print("Total:", total, "cached at:", time_cached)
    while total_left > 0:
        offset = total - total_left
        if total_left > 200:
            limit = 200
        else:
            limit = total_left
        all_chars_.extend(get_chars(offset, limit))
        total_left = total_left - limit
        print("# left:", total_left)
    print("Done")
    if dump:
        fname = "../../data/ladder_" + time.strftime("%Y%m%d-%H%M%S") + '.json.gz'
        print("Dumping to file: " + fname)
        with gzip.GzipFile(fname, 'w') as fout:
            fout.write(json.dumps(all_chars_).encode('utf-8'))
    return all_chars_


# Slow as molasses
def all_items(ladder_character_list, dump=False):
    url_get_items = 'https://www.pathofexile.com/character-window/get-items'
    url_get_jewels = 'https://www.pathofexile.com/character-window/get-passive-skills?reqData=0?'

    # Rate to do requests in seconds. Over 1.25 or something to not be rate limited. Solvable by doing larger requests?
    rate_limiter = 1.5

    """
    Eligible characters (not retired and above level 1)
    """
    characters_ = []
    for entry in ladder_character_list:
        if 'retired' not in entry.keys() and entry['character']['level'] > 1:
            characters_.append(entry)

    start_get = timer()
    total_ = len(characters_)
    print("Eligible characters:", total_)
    for i, character_ in enumerate(characters_):
        progress_ = round((i + 1) / total_ * 100, 2)
        time_left_ = (total_ - i) * 3
        print("Progress: {:=4}% Rank: {:=4} Character: {:23} Account: {:15} Estimated time left: {:8}."
              .format(progress_,
                      character_['rank'],
                      character_['character']['name'],
                      character_['account']['name'],
                      str(datetime.timedelta(seconds=time_left_))))

        param = {'accountName': character_['account']['name'], 'character': character_['character']['name']}

        # TODO: Be nice and do some fallback stuff, wrap request etc

        start = timer()
        character_['equipped'] = requests.get(url=url_get_items, params=param).json()
        end = timer()
        if (end - start) < rate_limiter:
            time.sleep(rate_limiter - (end - start))
        if 'error' in character_['equipped']:
            print(character_['account']['name'], character_['equipped']['error'])
        else:
            start = timer()
            character_['jewels'] = requests.get(url=url_get_jewels, params=param).json()
            end = timer()
            if (end - start) < rate_limiter:
                time.sleep(rate_limiter - (end - start))
            if 'error' in character_['jewels']:
                print(character_['account']['name'], character_['equipped']['error'])
    if dump:
        fname = "../../data/characters_" + time.strftime("%Y%m%d-%H%M%S") + '.json.gz'
        print("Dumping to file: " + fname)
        with gzip.GzipFile(fname, 'w') as fout:
            fout.write(json.dumps(characters_).encode('utf-8'))
    end_get = timer()
    print("Time spent getting", end_get - start_get)
    return characters_


def split_into_lists(char_account_items):
    gone_ = []
    rate_limit_ = []
    private_ = []
    other_ = []
    shame_ = []
    praise_ = []
    for char in char_account_items:
        if 'error' in char['equipped']:
            if char['equipped']['error']['code'] == 1:
                gone_.append(char)
            elif char['equipped']['error']['code'] == 2:
                other_.append(char)
            elif char['equipped']['error']['code'] == 3:
                rate_limit_.append(char)
            elif char['equipped']['error']['code'] == 4:
                other_.append(char)
            elif char['equipped']['error']['code'] == 5:
                other_.append(char)
            elif char['equipped']['error']['code'] == 6:
                private_.append(char)
            else:
                print("?", char)
        else:
            bad = False
            for item in char['equipped']['items']:
                if item['frameType'] != 3 and item['inventoryId'] != 'Flask':
                    bad = True
            for item in char['jewels']['items']:
                if item['frameType'] != 3:
                    bad = True
            if bad:
                shame_.append(char)
            else:
                praise_.append(char)
    return praise_, shame_, private_, gone_, other_, rate_limit_


def percent_of_tot(partial, tot):
    return round(len(partial) / len(tot) * 100, 2)

#
# if __name__ == "__main__":
#     # fn_test = '../test_data/test_chars.json'
#     #
#     # with open(fn_test) as json_file:
#     #     data = json.load(json_file)
#     # all_items = get_all_items(data, dump=False)
#     # with gzip.GzipFile(fn_json_gzip, 'r') as fin:
#     #     data = json.loads(fin.read().decode('utf-8'))
#     # # Slippery Hobo League(PL5357)
#     URL_tarke = "http://api.pathofexile.com/ladders/OneFreeSubEachAndEveryMonthBTW%20(PL4673)"
#     all_chars = all_chars_from_ladder(URL_tarke, dump=True)
#     all_items = all_items(all_chars, dump=True)
#     praise, shame, private, gone, other, rate_limit = split_into_lists(all_items)
#     if len(all_items):
#         print("Total characters                     :", len(all_items))
#         print("Praiseworthy(Probably naked)         :", len(praise), "   ,", percent_of_tot(praise, all_items), "%", )
#         print("Shameful                             :", len(shame), "  ,", percent_of_tot(shame, all_items), "%")
#         print("Private                              :", len(private), "   ,", percent_of_tot(private, all_items), "%")
#         print("Gone                                 :", len(gone), "  ,", percent_of_tot(gone, all_items), "%")
#         print("Rate Limited because I was ddosing   :", len(rate_limit), "  ,", percent_of_tot(rate_limit, all_items),
#               "%")
#     else:
#         print("Empty League")
#
#     # Read result all_char
#     # with open('data.json') as json_file:
#     #     data = json.load(json_file)
#
#     # # Read result all_items
#     # with open('../test_data/char_item.json') as json_file:
#     #     item_data = json.load(json_file)
