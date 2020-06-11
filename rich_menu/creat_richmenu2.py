# 菜單的
import requests
import json
from config import Config

headers = {"Authorization": "Bearer {}".format(Config.CHANNEL_ACCESS_TOKEN_SERVER), "Content-Type": "application/json"}

body = {
    "size": {"width": 2500, "height": 1686},
    "selected": "true",
    "name": "menu",
    "chatBarText": "功能選單",
    "areas": [
        {
            "bounds": {"x": 0, "y": 0, "width": 833, "height": 843},
            "action": {"type": "postback", "label": "訂單管理", "data": "訂單管理"}
        },
        {
            "bounds": {"x": 833, "y": 0, "width": 833, "height": 843},
            "action": {"type": "postback", "label": "功能待補", "data": "待補"}
        },
        {
            "bounds": {"x": 1686, "y": 0, "width": 833, "height": 843},
            "action": {"type": "postback", "label": "功能待補", "data": "待補"}
        },
        {
            "bounds": {"x": 0, "y": 843, "width": 833, "height": 843},
            "action": {"type": "uri", "uri": "https://liff.line.me/1654314321-Qjxerl9v"}
        },
        {
            "bounds": {"x": 833, "y": 843, "width": 833, "height": 843},
            "action": {"type": "postback", "label": "功能待補", "data": "待補"}
        },
        {
            "bounds": {"x": 1686, "y": 843, "width": 833, "height": 843},
            "action": {"type": "postback", "label": "功能待補", "data": "待補"}
        }
    ]
}

req = requests.request('POST', 'https://api.line.me/v2/bot/richmenu',
                       headers=headers, data=json.dumps(body).encode('utf-8'))

print(req.text)
