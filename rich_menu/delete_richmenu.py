from linebot import LineBotApi
from config import Config
from rich_menu import richmenu_list


line_bot_api = LineBotApi(Config.CHANNEL_ACCESS_TOKEN)

line_bot_api.delete_rich_menu('richmenu-b181ae67cff989ab3949e79676226331')

rich_menu_list = line_bot_api.get_rich_menu_list()

for rich_menu in rich_menu_list:
    print(rich_menu.rich_menu_id)
