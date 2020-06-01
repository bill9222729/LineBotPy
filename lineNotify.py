import requests


def lineNotifyMessage(token, msg):
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    payload = {'message': msg}
    r = requests.post("https://notify-api.line.me/api/notify", headers=headers, data=payload)
    return r.status_code


# 修改為你要傳送的訊息內容
message = '測試測試不要慌'
# 修改為你的權杖內容
token = 'yE1jIvfg8Y3cPLH5vFyCdzPDyIXUDuxjbgXuaDamFOQ'

lineNotifyMessage(token, message)
