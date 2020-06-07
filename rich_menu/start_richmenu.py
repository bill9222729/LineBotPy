import requests
from config import Config
from rich_menu import richmenu_list

headers = {"Authorization": "Bearer {}".format(Config.CHANNEL_ACCESS_TOKEN_SERVER), "Content-Type": "application/json"}
req = requests.request('POST',
                       'https://api.line.me/v2/bot/user/all/richmenu/{richmenu_id}'.format(
                           richmenu_id=richmenu_list.RichMenu_ID_Server.richmenu_01),
                       headers=headers)
print(req.text)
