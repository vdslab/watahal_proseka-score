import json

import requests

urls = list()
names = list()
for number in range(1,328):
    urls.append('https://proseka-trainer.com/music_scores/' + str(number).zfill(3) + '_m.json')
    names.append('song' + str(number))
# print(urls)
# print(names)
for i in range(0,327):
    data = requests.get(urls[i]).json()
    with open('datas/' + names[i] + '.json',mode='w') as f:
        json.dump(data,f)