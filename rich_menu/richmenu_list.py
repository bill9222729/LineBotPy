from linebot import LineBotApi
from config import Config

line_bot_api = LineBotApi(Config.CHANNEL_ACCESS_TOKEN)

rich_menu_list = line_bot_api.get_rich_menu_list()

for rich_menu in rich_menu_list:
    print(rich_menu.rich_menu_id)


class RichMenu_ID:
    richmenu_01 = 'richmenu-d83b96f72ce1216a5737470b40abb745'  # 還沒加入會員的預設richmenu
    richmenu_02 = 'richmenu-b0b9f4a8ec8475e006fe8ffab4b8a12f'  # 輸入小撇步
    richmenu_03 = 'richmenu-b4d280ab60751ab7d5b8a22761bc0c81'  # 加入會員後的功能選單
    richmenu_04 = 'richmenu-b8f95775f2a9ee64bccd2190742b7d4f'  # 最新的功能選單


class RichMenu_ID_Server:
    richmenu_01 = 'richmenu-c5b859d3f7fa081399398584e1c94357'  # 功能列表
    #richmenu-1461da339dc0332083c17fd944678eae
