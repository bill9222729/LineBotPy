# 加入會員的
import requests
import json
from config import Config


def creat_richmenu(CHANNEL_ACCESS_TOKEN):
    headers = {"Authorization": "Bearer {}".format(CHANNEL_ACCESS_TOKEN),
               "Content-Type": "application/json"}

    body = {
        "size": {"width": 2500, "height": 1686},
        "selected": "true",
        "name": "功能列表",
        "chatBarText": "功能列表",
        "areas": [
            {
                "bounds": {"x": 0, "y": 0, "width": 2500, "height": 1686},
                "action": {"type": "postback", "label": "", "data": "功能列表"}
            }
        ]
    }

    req = requests.request('POST', 'https://api.line.me/v2/bot/richmenu',
                           headers=headers, data=json.dumps(body).encode('utf-8'))

    print(req.text)


creat_richmenu(Config.CHANNEL_ACCESS_TOKEN_SERVER)
