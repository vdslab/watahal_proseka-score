import requests
import re
import json
from scrapy.selector import Selector

html = ''
with open('html.txt',encoding='utf-8') as f:
    html = f.read()

print(type(html))

count = 331

urls = list()
names = list()
datas = []

for i in range(1,count+1):
    urls.append('https://proseka-trainer.com/music_scores/' + str(i).zfill(3) + '_m.json')
    names.append('song' + str(i))
# print(urls)
# print(names)

for i in range(1,count+1):
    name = ''.join(Selector(text=html).css('#list>#song'+str(i)+'>.song>.songRowFrame>.songRow>.songName').get())
    # print(name)
    name = re.sub('<.*?>','',name)
    # print(name)
    level = Selector(text=html).css('#list>#song'+str(i)+'>.song>.songRowFrame>.songRow>.songLevel').get()
    # print(level)
    level = re.sub('<.*?>','',level)
    # print(level)
    bpm = Selector(text=html).css('#list>#song'+str(i)+'>.song>.songRowFrame>.songRow>.bpmText').get()
    # print(bpm)
    bpm = re.sub('<.*?>','',bpm)
    bpm = re.sub('BPM ','',bpm)
    # print(bpm)
    time = Selector(text=html).css('#list>#song'+str(i)+'>.song>.songRowFrame>.songRow>.timeBarFrame>.timeLayer.textLayer').get()
    # print(time)
    time = re.sub('<.*?>','',time)
    # print(time)
    times = time.split(':')
    # print(times)
    sec = int(times[0])*60+int(times[1])
    # print(sec)
    datas.append({'id':i,'name':name,'level':int(level),'bpm':int(bpm),'sec':sec})
with open('./data/detail/data.json',mode='w',encoding='utf-8') as f:
    json.dump(datas,f,ensure_ascii=False,indent=2,)

for i in range(0,count):
    data = requests.get(urls[i]).json()
    with open('./data/' + names[i] + '.json',mode='w') as f:
        json.dump(data,f,indent=2)