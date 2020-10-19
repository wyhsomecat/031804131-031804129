import requests

url="http://47.102.118.1:8089/api/challenge/create"

postdata = {
    "teamid": 30,
    "data": {
        "letter": "P",
        "exclude": 9,
        "challenge": [
            [8, 3, 6],
            [1, 2, 4],
            [7, 5, 0]
        ],
        "step": 12,
        "swap": [4,6]
    },
    "token": "8e1e6efb-60a7-4b54-a87c-8f6c784791b6"
}

r = requests.post(url,json=postdata)
print(r.text)