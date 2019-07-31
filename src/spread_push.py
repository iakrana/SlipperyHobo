from datetime import datetime
import json
import gzip
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import src.get_from_ladder


scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']


def worksheet():
    credentials = ServiceAccountCredentials.from_json_keyfile_name('../../oops.json', scope)
    gc = gspread.authorize(credentials)
    wks = gc.open("test")
    sheet = gc.open("test").sheet1
    return wks, sheet


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
        8: 'prophcy',
        9: 'relic',
    }
    return rarity[framtype]


def offending_items_string(shamed_accounts):
    lts = ""
    for char_ in shamed_accounts:
        lts = lts + \
            char_['character']['name'] + ',' + \
            char_['account']['name'] + ',' + \
            datetime.now().strftime("%Y/%m/%d, %H:%M:%S") + ',' + \
            'https://www.pathofexile.com/account/view-profile/' + \
            char_['account']['name'] + '/characters' + "\n"
        for item_ in char_['equipped']['items']:
            if item_['frameType'] != 3 and item_['inventoryId'] != 'Flask':
                lts = lts +\
                      ',' + item_['name'] +\
                      ',' + item_['typeLine'] +\
                      ',' + item_['inventoryId'] +\
                      ',' + frame_type_to_rarity(item_['frameType']) +\
                      ',' + item_['icon'] + ',' + item_['id'] +\
                      '\n'
        for item_ in char_['jewels']['items']:
            if item_['frameType'] != 3:
                lts = lts +\
                      ',' + item_['name'] +\
                      ',' + item_['typeLine'] +\
                      ',' + item_['inventoryId'] + \
                      ',' + frame_type_to_rarity(item_['frameType']) + \
                      ',' + item_['icon'] +\
                      ',' + item_['id'] +\
                      '\n'
        lts = lts + "\n"
    return lts


if __name__ == "__main__":
    fname = "../../data/characters_20190731-145653.json.gz"
    with gzip.GzipFile(fname, 'r') as fin:
        data = json.loads(fin.read().decode('utf-8'))

    praise, shame, private, gone, other, rate_limit = src.get_from_ladder.split_into_lists(data)
    lts_ = offending_items_string(shame)
    # todo utf-8? unicode? UnicodeEncodeError: 'charmap' codec can't encode characters in position 289513-289514: character maps to <undefined>
    f = open('csvfile.csv', 'w')
    f.write(lts_)  # Give your csv text here.
    f.close()
# csv_string = spread_offending_items(shame)
# # gc.import_csv(wks.id, csv_string.encode('utf-8'))
# # # with open('people.csv', 'a+',  encoding="utf-8") as writeFile:
# # #     writeFile.write(csv_string)
