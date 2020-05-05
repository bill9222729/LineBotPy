import requests
from config import Config


def setRichmenu(richmenu_id):
    headers = {"Authorization": "Bearer {}".format(Config.CHANNEL_ACCESS_TOKEN), "Content-Type": "application/json"}
    req = requests.request('POST',
                           'https://api.line.me/v2/bot/user/all/richmenu/{richmenu_id}'.format(richmenu_id='richmenu-d83b96f72ce1216a5737470b40abb745'),
                           headers=headers)

    print(req.text)
