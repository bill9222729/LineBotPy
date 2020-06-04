import requests
from config import Config


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
token = 'JtYMKOLaaMj9uOav9QPAqPu63XqAimlUc2Gu3cZM1mk'


# lineNotifyMessage(token, message)


def getNotifyToken(AuthorizeCode, userId):
    body = {
        "grant_type": "authorization_code",
        "code": AuthorizeCode,
        "redirect_uri": Config.SERVER_URI+"/hookNotify?userid={userId}".format(userId=userId),
        "client_id": Config.NOTIFY_CLIENT_ID,
        "client_secret": Config.NOTIFY_CLIENT_SECRET
    }
    r = requests.post("https://notify-bot.line.me/oauth/token", data=body)
    return r.json()["access_token"]


# getNotifyToken("0mpDY2ul6vN2kPOVUsBApE","U47eb075cc6756bf9075f79c91a9925a0")
