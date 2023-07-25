import json
import unicodedata

data = []
videoData = []
with open('data/detail/data.json',encoding='utf-8') as f:
    data = json.load(f)
with open('data/detail/video.json',encoding='utf-8') as f:
    videoData = json.load(f)
print(data[:5])
for i in range(len(data)):
    data[i]["name"] = unicodedata.normalize("NFKC",data[i]["name"])
    videoData[i]["title"] = unicodedata.normalize("NFKC",videoData[i]["title"])
data = sorted(data,key=lambda data:data["name"])
print(data[:5])
print(videoData[:5])
videoData = sorted(videoData,key=lambda data:data["title"])
print(videoData[:5])
print(videoData[0]["title"]==data[0]["name"])
for i in range(len(data)):
    if videoData[i]["title"] == data[i]["name"]:
        data[i]["videoid"] = videoData[i]["videoid"]
    else:
        print(videoData[i]["title"],data[i]["name"])
        raise RuntimeError
# if len(data) == len(videoData):
#     for i in range(len(data)):
#         for l in range(len(videoData)):
#             if data[i]["name"] == videoData[l]["title"]:
#                 data[i]["videoid"] = videoData[i]["videoid"]
# else:
#     raise RuntimeError
print(data[0])
with open('data/detail/data.json',mode='w',encoding='utf-8') as f:
    json.dump(data,f,ensure_ascii=False,indent=2,)