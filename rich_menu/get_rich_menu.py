from linebot import LineBotApi
from config import Config
from rich_menu import richmenu_list


line_bot_api = LineBotApi(Config.CHANNEL_ACCESS_TOKEN)

rich_menu = line_bot_api.get_rich_menu(richmenu_list.RichMenu_ID.richmenu_01)

print(rich_menu)
