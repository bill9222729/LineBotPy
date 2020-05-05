# 菜單的
import requests
import json
from config import Config

headers = {"Authorization": "Bearer {}".format(Config.CHANNEL_ACCESS_TOKEN), "Content-Type": "application/json"}

body = {
    "size": {"width": 2500, "height": 1686},
    "selected": "true",
    "name": "menu",
    "chatBarText": "功能選單",
    "areas": [
        {
            "bounds": {"x": 0, "y": 0, "width": 833, "height": 843},
            "action": {"type": "postback", "label": "我要預約", "data": "預約訂位", "displayText": "我要預約"}
        },
        {
            "bounds": {"x": 833, "y": 0, "width": 833, "height": 843},
            "action": {"type": "postback", "label": "訂位管理", "data": "訂位管理", "displayText": "訂位管理"}
        },
        {
            "bounds": {"x": 1686, "y": 0, "width": 833, "height": 843},
            "action": {"type": "postback", "label": "先掃QRCODE開始幫您店內點餐", "data": "店內點餐"}
        },
        {
            "bounds": {"x": 0, "y": 843, "width": 833, "height": 843},
            "action": {"type": "postback", "label": "這是今天的外帶菜單", "data": "當日外帶"}
        },
        {
            "bounds": {"x": 833, "y": 843, "width": 833, "height": 843},
            "action": {"type": "postback", "label": "這個功能還在想", "data": "待補"}
        },
        {
            "bounds": {"x": 1686, "y": 843, "width": 833, "height": 843},
            "action": {"type": "postback", "label": "這是專屬於你的會員中心", "data": "會員中心"}
        }
    ]
}

req = requests.request('POST', 'https://api.line.me/v2/bot/richmenu',
                       headers=headers, data=json.dumps(body).encode('utf-8'))

print(req.text)
