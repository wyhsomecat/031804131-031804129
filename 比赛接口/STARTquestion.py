import requests
import json
import  base64
url = "http://47.102.118.1:8089/api/challenge/start/"     # 获取赛题的接口

teamdata = {
    "teamid":30,
    "token":"8e1e6efb-60a7-4b54-a87c-8f6c784791b6"
}

r = requests.post(url, json=teamdata)
r.raise_for_status()
r.encoding = r.apparent_encoding
datadir = json.loads(r.text)
img = base64.b64decode(datadir["data"]["img"])
data = datadir['data']
json_image = data['img']
chanceleft = datadir['chanceleft']
step = data['step']
swap = data['swap']
uuid = datadir['uuid']

print(datadir)
print(chanceleft)
print(step)
print(swap)
print(uuid)
