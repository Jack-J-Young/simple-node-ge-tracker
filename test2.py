import requests
import json

latest = requests.get('https://prices.runescape.wiki/api/v1/osrs/latest')
map = requests.get('https://prices.runescape.wiki/api/v1/osrs/mapping')
r5m = requests.get('https://prices.runescape.wiki/api/v1/osrs/5m')
r24h = requests.get('https://prices.runescape.wiki/api/v1/osrs/24h')


prices = json.loads(latest.content)['data']
maps = json.loads(map.content)
r5min = json.loads(r5m.content)['data']
r24hr = json.loads(r24h.content)['data']

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

for id in r24hr:
    addData(id, 'averages', r24hr[id])

for id in r5min:
    addData(id, 'current', r5min[id])



for id in data:
    dat = data[id]
    if 'averages' in dat and dat['averages']['avgHighPrice'] != None and dat['averages']['avgLowPrice'] != None:
        addData(id, 'flip-profit', dat['averages']['avgHighPrice'] - dat['averages']['avgLowPrice'] - dat['averages']['avgHighPrice']*0.01)
# data.items().filter(lambda x:'ha-profit' in x[1])

hasha = {}

for id in data:
    if 'item-data' in data[id] and not 'limit' in data[id]['item-data']:
        data[id]['item-data']['limit'] = limit
    if 'flip-profit' in data[id] and 'item-data' in data[id] and 'averages' in data[id] and data[id]['averages']['avgHighPrice']!= None and data[id]['averages']['lowPriceVolume']!= None and data[id]['averages']['lowPriceVolume']!= None and data[id]['averages']['avgHighPrice'] < 10000:
        hasha[id] = data[id]
test = sorted(hasha.items(), key=lambda x:x[1]['flip-profit'] * (x[1]['averages']['highPriceVolume'] + x[1]['averages']['lowPriceVolume']))

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
    print(f"{item[1]['item-data']['name']}; average h price: {item[1]['averages']['avgHighPrice']}, average l price: {item[1]['averages']['avgLowPrice']}, margin: {item[1]['averages']['avgHighPrice'] - item[1]['averages']['avgLowPrice'] - item[1]['averages']['avgHighPrice']*0.01}, limit: {item[1]['item-data']['limit']}")