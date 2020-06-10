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
                "bounds": {"x": 0, "y": 0, "width": 833, "height": 843},
                "action": {"type": "uri", "uri": "https://liff.line.me/1654173476-emvXlo37"}  # 預約訂位
            },
            {
                "bounds": {"x": 833, "y": 0, "width": 833, "height": 843},
                "action": {"type": "postback", "label": "訂單紀錄", "data": "訂單管理"}
            },
            {
                "bounds": {"x": 1686, "y": 0, "width": 833, "height": 843},
                "action": {"type": "postback", "label": "這些是今天的菜單", "data": "點餐"}
            },
            {
                "bounds": {"x": 0, "y": 843, "width": 833, "height": 843},
                "action": {"type": "uri", "uri": "https://liff.line.me/1654173476-vql6VGkn"}  # 意見回饋
            },
            {
                "bounds": {"x": 833, "y": 843, "width": 833, "height": 843},
                "action": {"type": "postback", "label": "這是專屬於你的會員中心", "data": "會員中心"}
            },
            {
                "bounds": {"x": 1686, "y": 843, "width": 833, "height": 843},
                "action": {"type": "uri", "uri": "https://liff.line.me/1654173476-7lybVOAP"}
            }

        ]
    }

    req = requests.request('POST', 'https://api.line.me/v2/bot/richmenu',
                           headers=headers, data=json.dumps(body).encode('utf-8'))

    print(req.text)


creat_richmenu(Config.CHANNEL_ACCESS_TOKEN)
