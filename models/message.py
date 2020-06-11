from linebot.models import *


class AllMessage:

    # 使用者剛追隨時的歡迎訊息
    @staticmethod
    def welcome_message():
        message = FlexSendMessage(alt_text='歡迎訊息', contents={
            "type": "bubble",
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "嗨，歡迎加入我們",
                        "size": "lg",
                        "weight": "bold",
                        "offsetStart": "10px",
                        "offsetTop": "5px"
                    },
                    {
                        "type": "text",
                        "text": "嗨，我是屎蛋，我不只會訂餐，還會幫你\n做很多事情ㄛ！先加入我們體驗更完善的\n服務吧！",
                        "wrap": True,
                        "size": "sm",
                        "decoration": "none",
                        "margin": "sm",
                        "offsetEnd": "10px",
                        "offsetStart": "10px",
                        "offsetTop": "5px"
                    },
                    {
                        "type": "button",
                        "action": {
                            "type": "postback",
                            "label": "加入我們",
                            "data": "join_us",
                            "displayText": "好阿阿"
                        },
                        "margin": "md",
                        "style": "primary",
                        "offsetTop": "5px",
                        "position": "relative",
                        "height": "sm"
                    }
                ]
            }
        })
        return message

    # 註冊中要求使用者輸入手機號碼的訊息
    @staticmethod
    def sign_cellphone():
        message = FlexSendMessage(alt_text='還沒加入我們?', contents={
            "type": "bubble",
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "輸入手機號碼",
                        "size": "lg",
                        "weight": "bold",
                        "offsetTop": "5px",
                        "offsetStart": "10px"
                    },
                    {
                        "type": "text",
                        "text": "我們利用手機號碼驗證您的身分，\n並於必要時聯絡使用",
                        "margin": "sm",
                        "size": "md",
                        "wrap": True,
                        "decoration": "none",
                        "offsetTop": "5px",
                        "offsetStart": "10px",
                        "offsetEnd": "10px"
                    },
                    {
                        "type": "button",
                        "action": {
                            "type": "postback",
                            "label": "取消輸入",
                            "data": "exit"
                        },
                        "margin": "md",
                        "offsetTop": "5px"
                    }
                ]
            }
        })
        return message

    # 輸入了錯誤的手機格式
    @staticmethod
    def error_cellphone_format():
        message = FlexSendMessage(alt_text='號碼格式錯誤', contents={
            "type": "bubble",
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "錯誤的手機格式",
                        "size": "lg",
                        "weight": "bold",
                        "offsetStart": "10px",
                        "offsetTop": "5px"
                    },
                    {
                        "type": "text",
                        "text": "正確的手機格式應該是0988111222",
                        "wrap": True,
                        "size": "md",
                        "decoration": "none",
                        "margin": "sm",
                        "offsetEnd": "10px",
                        "offsetStart": "10px",
                        "offsetTop": "5px"
                    },
                    {
                        "type": "button",
                        "action": {
                            "type": "postback",
                            "label": "取消輸入",
                            "data": "exit"
                        },
                        "margin": "md",
                        "offsetTop": "5px"
                    }
                ]
            }
        })
        return message

    # 開啟會員中心
    @staticmethod
    def member_center(query):
        message = FlexSendMessage(alt_text='會員中心', contents={
            "type": "carousel",
            "contents": [
                {
                    "type": "bubble",
                    "hero": {
                        "type": "image",
                        "url": "https://i.imgur.com/bZtyoDh.jpg",
                        "aspectRatio": "20:13",
                        "size": "full",
                        "aspectMode": "cover"
                    },
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "你的名稱",
                                "weight": "bold"
                            },
                            {
                                "type": "text",
                                "text": "{}".format(query.user_name_custom),
                                "offsetTop": "10px"
                            }
                        ],
                        "height": "130px"
                    },
                    "footer": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "button",
                                "action": {
                                    "type": "message",
                                    "label": "點我編輯",
                                    "text": "編輯使用者名稱"
                                }
                            }
                        ]
                    }
                },
                {
                    "type": "bubble",
                    "hero": {
                        "type": "image",
                        "url": "https://i.imgur.com/FxZtHz0.jpg",
                        "aspectRatio": "20:13",
                        "size": "full",
                        "aspectMode": "cover"
                    },
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "你的住家",
                                "weight": "bold"
                            },
                            {
                                "type": "text",
                                "text": "{}".format(
                                    query.home_address),
                                "offsetTop": "10px"
                            }
                        ],
                        "height": "130px"
                    },
                    "footer": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "button",
                                "action": {
                                    "type": "message",
                                    "label": "點我編輯",
                                    "text": "編輯住家"
                                }
                            }
                        ]
                    }
                },
                {
                    "type": "bubble",
                    "hero": {
                        "type": "image",
                        "url": "https://i.imgur.com/NaqdvcT.jpg",
                        "aspectRatio": "20:13",
                        "size": "full",
                        "aspectMode": "cover"
                    },
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "你的公司",
                                "weight": "bold"
                            },
                            {
                                "type": "text",
                                "text": "{}".format(
                                    query.company_address),
                                "offsetTop": "10px"
                            }
                        ],
                        "height": "130px"
                    },
                    "footer": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "button",
                                "action": {
                                    "type": "message",
                                    "label": "點我編輯",
                                    "text": "編輯公司"
                                }
                            }
                        ]
                    }
                }
            ]
        })
        return message

    # 編輯使用者名稱
    @staticmethod
    def edit_user_name():
        message = FlexSendMessage(alt_text='編輯使用者名稱', contents={
            "type": "bubble",
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "該如何稱呼你？",
                        "size": "lg",
                        "weight": "bold",
                        "offsetStart": "10px",
                        "offsetTop": "5px"
                    },
                    {
                        "type": "text",
                        "text": "取個好的名稱方便老闆認出你！你\n也可以隨時更換名稱",
                        "wrap": True,
                        "size": "md",
                        "decoration": "none",
                        "margin": "sm",
                        "offsetEnd": "10px",
                        "offsetStart": "10px",
                        "offsetTop": "5px"
                    },
                    {
                        "type": "button",
                        "action": {
                            "type": "postback",
                            "label": "取消輸入",
                            "data": "exit"
                        },
                        "margin": "md",
                        "offsetTop": "5px"
                    }
                ]
            }
        })
        return message

    # 編輯住家
    @staticmethod
    def edit_home_address():
        message = FlexSendMessage(alt_text='編輯住家', contents={
            "type": "bubble",
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "你住哪裡？",
                        "size": "lg",
                        "weight": "bold",
                        "offsetStart": "10px",
                        "offsetTop": "5px"
                    },
                    {
                        "type": "text",
                        "text": "設定一個住址或是大地標，下次出門\n就能快速買早餐",
                        "wrap": True,
                        "size": "md",
                        "decoration": "none",
                        "margin": "sm",
                        "offsetEnd": "10px",
                        "offsetStart": "10px",
                        "offsetTop": "5px"
                    },
                    {
                        "type": "button",
                        "action": {
                            "type": "postback",
                            "label": "取消輸入",
                            "data": "exit"
                        },
                        "margin": "md",
                        "offsetTop": "5px"
                    }
                ]
            }
        })
        return message

    # 編輯公司
    @staticmethod
    def edit_company_address():
        message = FlexSendMessage(alt_text='編輯公司', contents={
            "type": "bubble",
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "你在哪裡上班？",
                        "size": "lg",
                        "weight": "bold",
                        "offsetStart": "10px",
                        "offsetTop": "5px"
                    },
                    {
                        "type": "text",
                        "text": "設定一個公司地址或是大地標，下次\n上班前就能快速買早餐",
                        "wrap": True,
                        "size": "md",
                        "decoration": "none",
                        "margin": "sm",
                        "offsetEnd": "10px",
                        "offsetStart": "10px",
                        "offsetTop": "5px"
                    },
                    {
                        "type": "button",
                        "action": {
                            "type": "postback",
                            "label": "取消輸入",
                            "data": "exit"
                        },
                        "margin": "md",
                        "offsetTop": "5px"
                    }
                ]
            }
        })
        return message

    # Server的功能列表
    @staticmethod
    def Menu():
        message = FlexSendMessage(alt_text='功能列表', contents={
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "button",
                        "action": {
                            "type": "uri",
                            "label": "發送公告",
                            "uri": "https://liff.line.me/1654314321-Qjxerl9v",
                        }
                    }
                ]
            }
        })
        return message

    # Client的功能列表
    @staticmethod
    def Menu_client(userid):
        message = FlexSendMessage(alt_text='功能列表', contents={
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "button",
                        "action": {
                            "type": "uri",
                            "label": "訂閱",
                            "uri": "https://e593cda5c426.ngrok.io/notify?userid={userid}".format(userid=userid)
                        }
                    },
                    {
                        "type": "button",
                        "action": {
                            "type": "uri",
                            "label": "會員中心",
                            "uri": "https://liff.line.me/1654173476-GO8zxXn6"
                        }
                    },
                    {
                        "type": "button",
                        "action": {
                            "type": "uri",
                            "label": "訂位",
                            "uri": "https://liff.line.me/1654173476-emvXlo37"
                        }
                    }
                ]
            }
        })
        return message

    # server 的確認訂單
    @staticmethod
    def confirmMessage(args_dic):
        message = FlexSendMessage(
            alt_text='確定此次訂位資訊嗎?\n姓名: ' + args_dic['name'] + '\n預約日期: ' + args_dic['date'] + '\n預約時間: ' +
                     args_dic['time'] + "\n預約人數: " + args_dic['number'],
            position='absolute',
            contents={
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "訂位資訊",
                            "weight": "bold",
                            "color": "#1DB446",
                            "size": "sm"
                        },
                        {
                            "type": "text",
                            "text": "OrderBar-點吧",
                            "weight": "bold",
                            "size": "xxl",
                            "margin": "md"
                        },
                        {
                            "type": "text",
                            "text": "260宜蘭縣宜蘭市公園路347號",
                            "size": "xs",
                            "color": "#aaaaaa",
                            "wrap": True
                        },
                        {
                            "type": "separator",
                            "margin": "xxl"
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "margin": "xxl",
                            "spacing": "sm",
                            "contents": [
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "名稱：",
                                            "size": "sm",
                                            "color": "#555555",
                                            "flex": 0
                                        },
                                        {
                                            "type": "text",
                                            "text": args_dic['name'],
                                            "size": "sm",
                                            "color": "#111111",
                                            "align": "end"
                                        }
                                    ]
                                },
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "預約日期：",
                                            "size": "sm",
                                            "color": "#555555",
                                            "flex": 0
                                        },
                                        {
                                            "type": "text",
                                            "text": args_dic['date'],
                                            "size": "sm",
                                            "color": "#111111",
                                            "align": "end"
                                        }
                                    ]
                                },
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "預約時間：",
                                            "size": "sm",
                                            "color": "#555555",
                                            "flex": 0
                                        },
                                        {
                                            "type": "text",
                                            "text": args_dic['time'],
                                            "size": "sm",
                                            "color": "#111111",
                                            "align": "end"
                                        }
                                    ]
                                },
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "預約人數：",
                                            "size": "sm",
                                            "color": "#555555",
                                            "flex": 0
                                        },
                                        {
                                            "type": "text",
                                            "text": args_dic['number'],
                                            "size": "sm",
                                            "color": "#111111",
                                            "align": "end"
                                        }
                                    ]
                                },
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "聯絡電話：",
                                            "size": "sm",
                                            "color": "#555555",
                                            "flex": 0
                                        },
                                        {
                                            "type": "text",
                                            "text": args_dic['phone_number'],
                                            "size": "sm",
                                            "color": "#111111",
                                            "align": "end"
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "type": "separator",
                            "margin": "xxl"
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "margin": "md",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "訂位編號：",
                                    "size": "xs",
                                    "color": "#aaaaaa",
                                    "flex": 0
                                },
                                {
                                    "type": "text",
                                    "text": "#" + args_dic['id'],
                                    "color": "#aaaaaa",
                                    "size": "xs",
                                    "align": "start"
                                }
                            ]
                        }
                    ]
                },
                "footer": {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "button",
                            "action": {
                                "type": "postback",
                                "label": "接受訂單",
                                "data": 'yes ' + args_dic['name'] + " " + args_dic['date'] + " " + args_dic[
                                    'time'] + " " + args_dic['number'] + " " + args_dic['userid'] + " " + args_dic['id']
                            }
                        },
                        {
                            "type": "separator"
                        },
                        {
                            "type": "button",
                            "action": {
                                "type": "postback",
                                "label": "拒絕",
                                "data": 'no ' + args_dic['name'] + " " + args_dic['date'] + " " + args_dic[
                                    'time'] + " " + args_dic['number'] + " " + args_dic['userid'] + " " + args_dic['id']
                            }
                        }
                    ]
                },
                "styles": {
                    "footer": {
                        "separator": True
                    }
                }
            }
        )

        return message

    # client的接受訂單
    # args_dic['name'] = order_data[1]
    # args_dic['date'] = order_data[2]
    # args_dic['time'] = order_data[3]
    # args_dic['num_people'] = order_data[4]
    @staticmethod
    def Order_Message(args_dic):
        message = FlexSendMessage(
            alt_text='訂位成功!!',
            position='absolute',
            contents={
                'type': 'bubble', 'direction': 'ltr',
                'body': {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "[訂位成功]",
                            "size": "md",
                            # "align": "center",
                            "margin": "md",
                            "color": "#3855FF"
                        },
                        {
                            "type": "text",
                            "text": "姓名 : " + args_dic['name'],
                            "size": "md",
                            # "align": "center",
                            "margin": "md",
                            "color": "#905c44"
                        },
                        {
                            "type": "text",
                            "text": "預定日期 : " + args_dic['date'],
                            "size": "md",
                            # "align": "center",
                            "margin": "md",
                            "color": "#905c44"
                        },
                        {
                            "type": "text",
                            "text": "預定時間 : " + args_dic['time'],
                            "size": "md",
                            # "align": "center",
                            "margin": "md",
                            "color": "#905c44"
                        },
                        {
                            "type": "text",
                            "text": "預約人數 : " + args_dic['num_people'],
                            "size": "md",
                            # "align": "center",
                            "margin": "md",
                            "color": "#905c44"
                        },
                        {
                            "type": "text",
                            "text": "預約順位 : 1",
                            "size": "md",
                            # "align": "center",
                            "margin": "md",
                            "color": "#905c44"
                        },
                        # {
                        # "type": "text",
                        # "text": "預約位置 : " + dict_doc['selected_seat'],
                        # "size": "md",
                        # "align": "center",
                        # "margin": "md",
                        # "color": "#905c44"
                        # },
                        {
                            "type": "text",
                            "text": "訂位編號 : 1591693360554",
                            "size": "md",
                            # "align": "center",
                            "margin": "md",
                            "color": "#905c44"
                        }
                    ]
                },
                'footer': {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "spacer",
                            "size": "xl"
                        },
                        {
                            "type": "button",
                            "style": "primary",
                            "color": "#905c44",
                            "action":
                                {
                                    "type": "message",
                                    "label": "我要取消預約",
                                    "text": '取消預約'
                                }
                        }
                    ]
                }
            }
        )

        return message
