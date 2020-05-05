# 加入會員的
import requests
import json
from config import Config

headers = {"Authorization": "Bearer {}".format(Config.CHANNEL_ACCESS_TOKEN), "Content-Type": "application/json"}

body = {
    "size": {"width": 2500, "height": 1686},
    "selected": "true",
    "name": "輸入小撇步",
    "chatBarText": "輸入小撇步",
    "areas": [
        {
            "bounds": {"x": 0, "y": 0, "width": 2500, "height": 1686},
            "action": {"type": "postback", "label": "", "data": "輸入小撇步"}
        }
    ]
}

req = requests.request('POST', 'https://api.line.me/v2/bot/richmenu',
                       headers=headers, data=json.dumps(body).encode('utf-8'))

print(req.text)
