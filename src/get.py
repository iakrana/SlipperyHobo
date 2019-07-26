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

# # Write result all_chars
# with open('data.json', 'w') as outfile:
#     json.dump(get_all_chars()[1], outfile)


# Read result all_char
with open('data.json') as json_file:
    data = json.load(json_file)


# slow as molassis
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


# Write result all_items
with open('param_item.json', 'w') as outfile:
    json.dump(get_all_items(data), outfile)


# Read result all_items
# with open('param_item.json') as json_file:
#     item_data = json.load(json_file)
#
#
# for char in item_data:
#     print(char)
    # for items in char['inventory']:
    #     for item in items:
    #         print(item)
            # if item['frameType'] == 3:
            #     print(char['accountName'], "Unique", item['inventoryId'], item['name'], item['category'], item['frameType'])

# items = item_data['items']
# for item in items:
#     if item['frameType'] == 3:
#         print("Unique", item['inventoryId'], item['name'], item['category'],  item['frameType'])
#

# worn_items_inventoryId = {
#     'Helm',
#     'Amulet',
#     'BodyArmour'
#     'Ring',
#     'Ring2',
#     'Gloves',
#     'Belt',
#     'Boots',
#     'Weapon',
#     'Offhand',
#     'Weapon2',
#     'Offhand2',
#     'Flask'
# }


