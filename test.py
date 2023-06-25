import requests
import json


headers = {
    'User-Agent': 'Personal ge tracker',
    'From': 'jackjordanyoung@gmail.com'  # This is another valid field
}

latest = requests.get('https://prices.runescape.wiki/api/v1/osrs/latest', headers=headers)
map = requests.get('https://prices.runescape.wiki/api/v1/osrs/mapping', headers=headers)
hr = requests.get('https://prices.runescape.wiki/api/v1/osrs/5m', headers=headers)

prices = json.loads(latest.content)['data']
maps = json.loads(map.content)
hour = json.loads(hr.content)['data']

limit = 500

data = {}

def addData(id, cat, dat):
    if not id in data:
        data[id] = {}
    
    data[id][cat] = dat

idmaps = {}
for item in maps:
    addData(f'{item["id"]}', 'item-data', item)

for id in prices:
    addData(id, 'prices', prices[id])

for id in hour:
    addData(id, 'averages', hour[id])



for id in data:
    dat = data[id]
    if 'item-data' in dat and 'averages' in dat and 'highalch' in dat['item-data'] and dat['averages']['avgHighPrice'] != None:
        addData(id, 'ha-profit', dat['item-data']['highalch'] - dat['averages']['avgHighPrice'] - 88)
# data.items().filter(lambda x:'ha-profit' in x[1])

hasha = {}

for id in data:
    if 'item-data' in data[id] and not 'limit' in data[id]['item-data']:
        data[id]['item-data']['limit'] = limit
    if 'ha-profit' in data[id]:
        hasha[id] = data[id]
test = sorted(hasha.items(), key=lambda x
              :x[1]['ha-profit'] * min(x[1]['item-data']['limit'], limit))

# amargin = {}
# for id in prices:
#     price = prices[id]
#     if price['low'] != None and price['high'] != None:
#         amargin[id] = (price['high'] - price['low']) - (price['high'] * 0.01)

# max = 0
# maxid = 0

# for id in amargin:
#     if amargin[id] > max and prices[id]['high'] < 480000:
#         max = amargin[id]
#         maxid = id

for item in test:
    print(f"{item[1]['item-data']['name']}; HAP: {item[1]['ha-profit']}, HA: {item[1]['item-data']['highalch']}, price: {item[1]['averages']['avgHighPrice']}, tProff: {item[1]['ha-profit']*min(item[1]['item-data']['limit'], limit)}, limit: {item[1]['item-data']['limit']}")