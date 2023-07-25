import json
import re

# with open('data/detail/data.json',encoding='utf-8') as f:
#     data = json.load(f)
# print(type(data))
# print(data)
data = []
with open('data/detail/videoData.json',encoding='utf-8') as f:
    data = json.load(f)
    # print(type(data))
    # print(data[0])
    for i in range(len(data)):
        a = data[i]["title"]
        # print(type(a))
        a = re.sub('\[.*?\]','',a)
        # print(a)
        a = re.sub('\(MASTER.*','',a)
        # print(a)
        a = a.strip()
        # print(a)
        data[i]["title"] = a
# print(data)
with open('data/detail/video.json',mode='w',encoding='utf-8') as f:
    json.dump(data,f,ensure_ascii=False,indent=2)