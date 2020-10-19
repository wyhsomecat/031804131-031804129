import requests
import json

url="http://47.102.118.1:8089/api/challenge/submit"
postdata = {
        "uuid": '',
    "teamid": 30 ,
    "token":"8e1e6efb-60a7-4b54-a87c-8f6c784791b6" ,
    "answer": {
        "operations":"",
        "swap": []
    }
}

r = requests.post(url,json=postdata)
r.raise_for_status()
print(r.text)

