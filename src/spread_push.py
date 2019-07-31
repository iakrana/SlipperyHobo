from datetime import datetime
import json
import gzip
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import src.get_from_ladder
from timeit import default_timer as timer
import time


def worksheet(wks_name_):
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('../../oops.json', scope)
    gc_ = gspread.authorize(credentials)

    wks_created_ = gc_.create(wks_name_)
    wks_created_.share('hobo-2@slipperyhobo.iam.gserviceaccount.com', perm_type='user', role='writer')
    wks_created_.share('anarkai@gmail.com', perm_type='user', role='writer')
    wks_ = gc_.open('shame')
    return gc_, wks_


def frame_type_to_rarity(framtype):
    rarity = {
        0: 'normal',
        1: 'magic',
        2: 'rare',
        3: 'unique',
        4: 'gem',
        5: 'currency',
        6: 'divination card',
        7: 'quest item',
        8: 'prophecy',
        9: 'relic',
    }
    return rarity[framtype]

# todo make list of lists and a stringify function


def offending_items_string(shamed_accounts, dump=False):
    lts = "Account Name, Character Name, DateTime, item name, typeLine, inventoryId, rarity, icon, char_link, twitch\n "
    for char_ in shamed_accounts:
        lts = lts + \
            char_['account']['name'] +\
            ',' + char_['character']['name'] + \
            ',' + datetime.now().strftime("%Y/%m/%d %H:%M:%S") + \
            ',' + ',' + ',' + ',' + ',' +\
            ',' + 'https://www.pathofexile.com/account/view-profile/' + char_['account']['name'] + '/characters' + \
            ',' + (char_['account']['twitch']['name'] if 'twitch' in char_['account'].keys() else "") + "\n"
        for item_ in char_['equipped']['items']:
            if item_['frameType'] != 3 and item_['inventoryId'] != 'Flask':
                lts = lts + char_['account']['name'] + \
                      ',' + char_['character']['name'] + \
                      ',' + datetime.now().strftime("%Y/%m/%d %H:%M:%S") + \
                      ',' + item_['name'] + \
                      ',' + item_['typeLine'] +\
                      ',' + item_['inventoryId'] +\
                      ',' + frame_type_to_rarity(item_['frameType']) +\
                      ',' + item_['icon'] + ',' + item_['id'] +\
                      '\n'
        for item_ in char_['jewels']['items']:
            if item_['frameType'] != 3:
                lts = lts + char_['account']['name'] + \
                      ',' + char_['character']['name'] + \
                      ',' + datetime.now().strftime("%Y/%m/%d %H:%M:%S") + \
                      ',' + item_['name'] + \
                      ',' + item_['typeLine'] +\
                      ',' + item_['inventoryId'] + \
                      ',' + frame_type_to_rarity(item_['frameType']) + \
                      ',' + item_['icon'] +\
                      ',' + item_['id'] +\
                      '\n'
        lts = lts + "\n"
    if dump:
        with open('../../data/shame_' + time.strftime("%Y%m%d-%H%M%S") + '.csv', 'w',  encoding="utf-8") as writeFile:
            writeFile.write(csv_string)
    return lts


def write_result_google_sheet(csv_string_, private_list_, wks_name_):
    gc_, wks_ = worksheet(wks_name_)
    gc_.import_csv(wks_.id, csv_string_.encode('utf-8'))

    private_accounts = list(dict.fromkeys([char['account']['name'] for char in private_list_]))
    pvt_sheet = wks_.add_worksheet(title="private list", rows='1', cols=len(private_accounts))
    pvt_sheet.insert_row(private_accounts, 1)


if __name__ == "__main__":
    # testing
    start = timer()
    fname = "../../data/characters_20190731-145653.json.gz"
    with gzip.GzipFile(fname, 'r') as fin:
        data = json.loads(fin.read().decode('utf-8'))
    end = timer()
    print("zip timer", end - start)
    start = timer()
    praise, shame, private, gone, other, rate_limit = src.get_from_ladder.split_into_lists(data)
    end = timer()
    print("split timer", end - start)
    start = timer()
    csv_string = offending_items_string(shame)
    end = timer()
    write_result_google_sheet(csv_string, private, time.strftime("%Y-%m-%d"))
