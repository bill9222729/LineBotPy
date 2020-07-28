"""
這是昀葦加ㄉ
"""
import datetime
import json

import requests
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, request, abort, redirect, render_template, jsonify

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from library.linebot.models import *

from urllib.parse import parse_qsl
import uuid

# 匯入richmenu清單
from library.linebot.models.send_messages import Sender

from models.scheduler import check_database
from rich_menu import richmenu_list
# 匯入正規則表達
import re
# 匯入各種的自訂訊息
from models.message import AllMessage
# 匯入設定檔
from config import Config
# 匯入資料庫
from database import db_session, init_db
from models.user import User
from models.product import Products
# 匯入購物車
from models.cart import Cart
# 匯入訂單模組
from models.order import Orders
# 匯入訂單內的商品模組
from models.item import Items
# 匯入訂位模組
from models.booking import Booking
# 匯入linepay模組
from models.linepay import LinePay
# 匯入Notify模組
from models import lineNotify
# 匯入情感分析API
from models import SentimentAnalysis
# 匯入時間模組
from datetime import datetime

app = Flask(__name__)

# client的
line_bot_api = LineBotApi(Config.CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(Config.CHANNEL_SECRET)

# server的
line_bot_api_server = LineBotApi(Config.CHANNEL_ACCESS_TOKEN_SERVER)
handler_server = WebhookHandler(Config.CHANNEL_SECRET_SERVER)

# 出大絕直接設定全域變數給付款連結dd
PAY_WEB_URL = ''


# 當連線中斷時自動關閉資料庫
# 資料內容來自https://flask.palletsprojects.com/en/1.1.x/patterns/sqlalchemy/
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

@app.route("/haha")
def haha():
    return "haha"
# 測試用
@app.route('/sendjson', methods=['POST'])
def sendjson():
    # 接受前端发来的数据
    data = json.loads(request.form.get('data'))
    # lesson: "Operation System"
    # score: 100
    lesson = data["lesson"]
    score = data["score"]
    # 自己在本地组装成Json格式,用到了flask的jsonify方法
    info = dict()
    info['name'] = "pengshuang"
    info['lesson'] = lesson
    info['score'] = score
    return jsonify(info)


# 開啟QRCodeScanner
@app.route('/qrcode')
def scanner():
    return render_template("qrcode.html")


# 意見回饋
@app.route('/feedback')
def feedback():
    return render_template(r'feedback.html')


# 情感分析
@app.route('/sentimentAnalysis', methods=['POST'])
def sentimentAnalysis():
    # 取得來自前端的JSON資料
    data = json.loads(request.form.get('data'))
    result = SentimentAnalysis.sentimentAnalysis(data['message'])
    data['score'] = result['score']
    data['magnitude'] = result['magnitude']
    sentiment = "中立"
    if (float(result['score']) > 0) and (float(result['score']) < 0.5):
        sentiment = "正面"
    elif (float(result['score']) < 0) and (float(result['score']) > -0.5):
        sentiment = "負面"
    elif (float(result['score']) > 0.5):
        sentiment = "非常正面"
    elif (float(result['score']) < -0.5):
        sentiment = "非常負面"
    line_bot_api_server.push_message('U47eb075cc6756bf9075f79c91a9925a0', TextSendMessage(text="[您有一則新回饋]\n回饋內容：\n" +
                                                                                               data[
                                                                                                   'message'] + "\n\nAI情緒分析結果：" +
                                                                                               sentiment))
    line_bot_api_server.push_message('U3f7562b0d0e0ffc22f3b82fa90af5a27', TextSendMessage(text="[您有一則新回饋]\n回饋內容：\n" +
                                                                                               data[
                                                                                                   'message'] + "\n\nAI情緒分析結果：" +
                                                                                               sentiment))
    line_bot_api_server.push_message('Ua64df883240f211c05bf798686b8217d', TextSendMessage(text="[您有一則新回饋]\n回饋內容：\n" +
                                                                                               data[
                                                                                                   'message'] + "\n\nAI情緒分析結果：" +
                                                                                               sentiment))
    line_bot_api_server.push_message('Uf172bde17bf332ad7060a417db99f1c2', TextSendMessage(text="[您有一則新回饋]\n回饋內容：\n" +
                                                                                               data[
                                                                                                   'message'] + "\n\nAI情緒分析結果：" +
                                                                                               sentiment))
    return jsonify(data)


# 訂位
@app.route('/booking')
def booking():
    return render_template(r"booking.html")


# 會員中心
@app.route('/profile')
def profile():
    return render_template(r"profile.html")


# 取得使用者資料
@app.route('/getUserProfile', methods=['POST'])
def getUserProfile():
    # 取得來自前端的JSON資料
    data = json.loads(request.form.get('data'))
    # 取得資料庫table=user的資料
    query = User.query.filter_by(id=data['user_id']).first()
    data['user_name_custom'] = query.user_name_custom
    data['home_address'] = query.home_address
    data['company_address'] = query.company_address
    data['phone_number'] = query.phone_number
    print(data)
    return jsonify(data)


# 寫入會員中心資料
@app.route('/setProfile', methods=['POST'])
def setProfile():
    # 取得來自前端的JSON資料
    data = json.loads(request.form.get('data'))
    # 取得資料庫table=user的資料
    query = User.query.filter_by(id=data['user_id']).first()
    # 判斷資料有更新就更新
    if data['user_name_custom'] != query.user_name_custom:
        query.user_name_custom = data['user_name_custom']
    if data['home_address'] != query.home_address:
        query.user_name_custom = data['home_address']
    if data['company_address'] != query.company_address:
        query.user_name_custom = data['company_address']
    if data['phone_number'] != query.phone_number:
        query.user_name_custom = data['phone_number']

    # 更新資料庫
    db_session.commit()
    return "OK"


# LIFF的範例文件
@app.route('/index')
def index():
    # 路徑不須加 templates
    return render_template(r"index.html")


# Cookie測試
@app.route('/cookie')
def cookie():
    return render_template(r"cookie.html")


# sqlite測試
@app.route('/sqltest')
def sqlTest():
    return render_template(r"sqltest.html")


@app.route("/liff", methods=['GET'])
def liff():
    print("注意")
    redirect_url = request.args.get('liff.state')
    print(request.args)
    print(type(request.args))
    print(redirect_url.split('=', 1)[1])
    return redirect(redirect_url.split('=', 1)[1])


# linepay的confirm
@app.route("/confirm")
def confirm():
    transaction_id = request.args.get('transactionId')
    order = db_session.query(Orders).filter(Orders.transaction_id == transaction_id).first()

    if order:
        line_pay = LinePay()
        line_pay.confirm(transaction_id=transaction_id, amount=order.amount)

        order.is_pay = True
        db_session.commit()

        message = order.display_receipt()
        line_bot_api.push_message(order.user_id, message)
        return '<h1>你的訂單已經完成付款,感謝您的訂購</h1>'


# notify連動按鈕
@app.route('/notify')
def notify():
    userId = request.args.get('userid')
    server_url = Config.SERVER_URI
    return render_template(r"notify.html", userId=userId, server_url=server_url)


# notify連動成功
@app.route("/hookNotify")
def hookNotify():
    authorizeCode = request.args.get('code')
    userId = request.args.get('userid')
    token = lineNotify.getNotifyToken(authorizeCode, userId)
    query = User.query.filter_by(id=userId).first()
    query.notifyToken = token
    db_session.commit()
    lineNotify.lineNotifyMessage(token, "從今以後你就成為我們廣播的俘虜ㄌ")
    return 'OK'


# notify發送公告頁面
@app.route("/sendNotify")
def sendNotifyPage():
    return render_template(r"sendNotify.html")


# notify發送公告
@app.route("/sendNotify", methods=['POST'])
def sendNotify():
    # 取得來自前端的JSON資料
    data = json.loads(request.form.get('data'))
    query = User.query
    for user in query:
        if user.notifyToken != None:
            lineNotify.lineNotifyMessage(user.notifyToken, "\n  " + data["message"])
    print(data)
    return 'OK'


# server的callback
@app.route("/server_callback", methods=['POST'])
def callback_server():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    print(body)

    # handle webhook body
    try:
        handler_server.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler_server.add(MessageEvent, message=TextMessage)
def handle_message_server(event):
    # 從event裡面取得用戶id
    user_id = event.source.user_id
    # 從event裡面取得reply_token
    reply_token = event.reply_token
    # 從資料庫取得送出postback的用戶資料
    query = User.query.filter_by(id=user_id).first()
    # 從event裡面取得用戶傳來的訊息
    message_text = str(event.message.text).lower()
    # 建立一個購物車物件
    cart = Cart(user_id=user_id)

    # 綁webhook
    if reply_token == '00000000000000000000000000000000':
        return 'ok'

    line_bot_api_server.reply_message(reply_token, TextSendMessage(text=message_text))


@handler_server.add(PostbackEvent)
def handler_postback_server(event):
    # 把postback裡面的資料轉成字典
    data = dict(parse_qsl(event.postback.data))
    # 再取出action裡面的值
    action = data.get('action')
    # 從event裡面取得用戶id
    user_id = event.source.user_id
    # 從event裡面取得reply_token
    reply_token = event.reply_token
    # 從資料庫取得送出postback的用戶資料
    query = User.query.filter_by(id=user_id).first()
    if event.postback.data in ['功能列表']:
        line_bot_api_server.reply_message(reply_token, messages=AllMessage.Menu())
        return

    # 如果接收訂單
    if 'yes' in event.postback.data:
        order_data = str(event.postback.data).split(" ")
        booking_info = Booking.query.filter_by(id=order_data[6]).first()
        print(booking_info.id)
        # 如果訂單已經被處理過了
        if booking_info.is_confirm != 0:
            line_bot_api_server.reply_message(reply_token, TextSendMessage(text="這張單子已經處理過了ㄛ！"))
            return
        # 給老闆一點回饋
        line_bot_api_server.reply_message(reply_token, TextSendMessage(text="成功接受訂單"))

        # 建立參數字典
        args_dic = {}
        args_dic['name'] = order_data[1]
        args_dic['date'] = order_data[2]
        args_dic['time'] = order_data[3]
        args_dic['num_people'] = order_data[4]
        args_dic['phone_number'] = query.phone_number
        args_dic['id'] = booking_info.id
        user_id = order_data[5]

        print(args_dic)

        # 把訂單確認狀態改成1(接單)
        booking_info.is_confirm = 1
        db_session.commit()

        print(event.postback.data)
        line_bot_api.push_message(user_id, AllMessage.Order_Message(args_dic))
        return

    # 如果拒絕訂單
    if 'no' in event.postback.data:
        # 先把參數拆開
        order_data = str(event.postback.data).split(" ")
        booking_info = Booking.query.filter_by(id=order_data[6]).first()

        # 如果訂單已經被處理過了
        if booking_info.is_confirm != 0:
            line_bot_api_server.reply_message(reply_token, TextSendMessage(text="這張單子已經處理過了ㄛ！"))
            return
        # 給老闆一點回饋
        line_bot_api_server.reply_message(reply_token, TextSendMessage(text="已拒絕訂單"))

        # 把訂單確認狀態改成-1(拒絕)
        booking_info.is_confirm = -1
        db_session.commit()

        user_id = str(event.postback.data).split(" ")[5]
        line_bot_api.push_message(user_id, TextSendMessage(text="店家拒絕此次訂位!\n麻煩請於上方選時間處選其它時刻，感謝您~"))
        return

    if event.postback.data in ['訂單管理']:
        print('訂單管理')
        line_bot_api_server.reply_message(reply_token, messages=Booking.list_all_manager())
        return


# client的callback
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    print(body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 從event裡面取得用戶id
    user_id = event.source.user_id
    # 從event裡面取得reply_token
    reply_token = event.reply_token
    # 從資料庫取得送出postback的用戶資料
    query = User.query.filter_by(id=user_id).first()
    # 從event裡面取得用戶傳來的訊息
    message_text = str(event.message.text).lower()
    # 建立一個購物車物件
    cart = Cart(user_id=user_id)

    # 綁webhook
    if reply_token == '00000000000000000000000000000000':
        return 'ok'

    # 如果正在註冊中
    if query.is_signup:
        if check_cellphone(event.message.text):
            line_bot_api.push_message(user_id, TextSendMessage('恭喜註冊成功！'))
            line_bot_api.link_rich_menu_to_user(user_id, richmenu_list.RichMenu_ID.richmenu_04)
            query.is_member = True
            query.is_signup = False
            query.phone_number = event.message.text
            db_session.commit()
            return
        else:
            line_bot_api.push_message(user_id, AllMessage.error_cellphone_format())

    if query.is_member:

        if query.edit_user_name:
            print('編輯使用者中')
            query.user_name_custom = message_text
            query.edit_user_name = False
            db_session.commit()
            line_bot_api.push_message(user_id, TextSendMessage(text='設定完成'))
            return
        elif query.edit_home_address:
            print('編輯住家中')
            query.home_address = message_text
            query.edit_home_address = False
            db_session.commit()
            line_bot_api.push_message(user_id, TextSendMessage(text='設定完成'))
            return
        elif query.edit_company_address:
            print('編輯公司中')
            query.company_address = message_text
            query.edit_company_address = False
            db_session.commit()
            line_bot_api.push_message(user_id, TextSendMessage(text='設定完成'))
            return

        # 編輯使用者名稱
        if message_text == '編輯使用者名稱':
            query.edit_user_name = True
            query.edit_home_address = False
            query.edit_company_address = False
            db_session.commit()
            line_bot_api.reply_message(event.reply_token, AllMessage.edit_user_name())
            return
        # 編輯住家
        elif message_text == '編輯住家':
            query.edit_user_name = False
            query.edit_home_address = True
            query.edit_company_address = False
            db_session.commit()
            line_bot_api.reply_message(event.reply_token, AllMessage.edit_home_address())
            return
        # 編輯公司
        elif message_text == '編輯公司':
            query.edit_user_name = False
            query.edit_home_address = False
            query.edit_company_address = True
            db_session.commit()
            line_bot_api.reply_message(event.reply_token, AllMessage.edit_company_address())
            return

        # 購物車相關
        if "數量為:" in message_text:
            product_name = message_text.split(',')[0]
            num_item = message_text.rsplit(':')[1]

            product = db_session.query(Products).filter(Products.name.ilike(product_name)).first()

            if product:

                cart.add(product=product_name, num=num_item)

                confirm_template = ConfirmTemplate(
                    text='{},數量為:{}?'.format(product_name, num_item),
                    actions=[
                        PostbackAction(label='繼續選購', text='繼續選購', data='當日外帶'),
                        PostbackAction(label='確認訂單', text='確認訂單', data='確認訂單')
                    ])

                line_bot_api.reply_message(reply_token,
                                           TemplateSendMessage(alt_text='還需要加購嗎?', template=confirm_template))

            else:
                line_bot_api.reply_message(reply_token, TextSendMessage(text="抱歉,我們沒有賣{}".format(product_name)))

        # 功能列表
        if message_text == "功能列表":
            line_bot_api.reply_message(reply_token, AllMessage.Menu_client(user_id))
            return

        # 變成管理員的通關密碼
        if message_text in ["霹靂卡霹靂拉拉波波莉娜貝貝魯多", "AI戰神"]:
            query.is_manager = True
            line_bot_api.reply_message(reply_token, TextSendMessage(text="恭喜你成為管理員了"))
            return

        # # 其他
        # # 使用客青雲的API取得回應內容
        # r = requests.get("http://api.qingyunke.com/api.php?key=free&appid=0&msg=" + message_text)
        # msg = eval(r.text)['content']
        # # 使用繁化姬來簡轉繁
        # rr = requests.get("https://api.zhconvert.org/convert?text={msg}&converter=Taiwan".format(msg=msg))
        # msg_Taiwan = json.loads(rr.text)
        # # 回應使用者
        # line_bot_api.reply_message(reply_token, TextSendMessage(text=msg_Taiwan['data']['text']))

# 收到語音訊息
@handler.add(MessageEvent, message=AudioMessage)
def handle_audio_message(event):
    print(event)

# 收到圖片訊息
@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    print(event)
    # 從event裡面取得用戶id
    user_id = event.source.user_id
    # 想辦法抓出圖片網址裡的action
    message_json = json.loads(str(event.message))
    message_url = str(message_json['contentProvider']['originalContentUrl'])
    message_url_args = message_url.split('?')[1].split('&')
    args_dic = {}
    for x in message_url_args:
        args_dic[x.split("=")[0]] = x.split("=")[1]
    # 從event裡面取得reply_token
    reply_token = event.reply_token
    # 從資料庫取得送出postback的用戶資料
    query = User.query.filter_by(id=user_id).first()
    args_dic['name'] = query.user_name_custom
    args_dic['phone_number'] = query.phone_number
    args_dic['userid'] = user_id
    if args_dic['action'] == 'booking':
        # 老師說的對，先不要用UUID先用日期檔老師一下
        # 等之後再修回來
        # # 用uuid創一個訂單編號
        # booking_id = uuid.uuid4().hex
        booking_id = str(datetime.today().strftime('%Y%m%d%H%M%S'))

        # 存入字典
        args_dic['id'] = booking_id
        date_string = args_dic['date'] + " " + args_dic['time'] + ":01"
        date_time = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
        booking = Booking(id=booking_id,
                          book_time=date_time,
                          is_confirm=0,
                          user_id=user_id,
                          people_num=args_dic['number'])
        db_session.add(booking)
        db_session.commit()
        line_bot_api_server.push_message('U47eb075cc6756bf9075f79c91a9925a0',
                                         AllMessage.confirmMessage(args_dic))
        line_bot_api_server.push_message('Uf172bde17bf332ad7060a417db99f1c2',
                                         AllMessage.confirmMessage(args_dic)),
        line_bot_api_server.push_message('U3f7562b0d0e0ffc22f3b82fa90af5a27',
                                         AllMessage.confirmMessage(args_dic))
        print(args_dic)
        return

    if args_dic['action'] == 'order':
        line_bot_api.reply_message(reply_token, TextSendMessage(text="好的，" + args_dic["table"] + "是嗎?\n以下是我們的菜單！"))
        line_bot_api.push_message(user_id, Products.list_all())


@handler.add(PostbackEvent)
def handler_postback(event):
    # 把postback裡面的資料轉成字典
    data = dict(parse_qsl(event.postback.data))
    # 再取出action裡面的值
    action = data.get('action')
    # 從event裡面取得用戶id
    user_id = event.source.user_id
    # 從event裡面取得reply_token
    reply_token = event.reply_token
    # 建立一個購物車物件
    cart = Cart(user_id=user_id)
    # 從資料庫取得送出postback的用戶資料
    query = User.query.filter_by(id=user_id).first()
    print(event.postback.data)
    # 點擊加入會員
    if event.postback.data in ['join_us', '加入會員']:
        # 資料庫該使用者狀態改為註冊中
        # Updata data
        print('註冊中')
        query.is_signup = True
        db_session.commit()
        line_bot_api.link_rich_menu_to_user(user_id, richmenu_list.RichMenu_ID.richmenu_02)
        line_bot_api.push_message(user_id, AllMessage.sign_cellphone())
    # 點擊取消輸入之類的
    elif event.postback.data in ['exit']:
        query.is_signup = False
        query.edit_user_name = False
        query.edit_home_address = False
        query.edit_company_address = False
        db_session.commit()
        if not query.is_member:
            line_bot_api.link_rich_menu_to_user(user_id, richmenu_list.RichMenu_ID.richmenu_01)
        line_bot_api.push_message(user_id, TextSendMessage(text='好的，歡迎您再來找我聊聊天喔！'))
    # 點擊會員中心
    elif event.postback.data in ['會員中心']:
        line_bot_api.reply_message(reply_token, TextSendMessage(text='這是專屬於你的會員中心', sender=Sender(
            name='會員中心管理員結衣',
            icon_url='https://i.imgur.com/S7SHmup.png'
        )))
        line_bot_api.push_message(user_id, AllMessage.member_center(query))
    # 觸發點餐相關事件
    elif event.postback.data in ['當日外帶', 'add', '點餐']:
        # 先跳出選擇內用外帶
        line_bot_api.reply_message(reply_token, TemplateSendMessage(alt_text="請問您要內用還是外帶呢？",
                                                                    sender=Sender(
                                                                        name='服務員結衣',
                                                                        icon_url='https://i.imgur.com/S7SHmup.png'
                                                                    ),
                                                                    template=ConfirmTemplate(
                                                                        text="請問您要內用還是外帶呢？",
                                                                        actions=[
                                                                            PostbackAction(
                                                                                label="內用",
                                                                                text="內用",
                                                                                data="here"
                                                                            ),
                                                                            PostbackAction(
                                                                                label="外帶",
                                                                                text="外帶",
                                                                                data="out"
                                                                            )
                                                                        ]
                                                                    )))
    # 外帶事件
    elif event.postback.data in ['out']:
        line_bot_api.reply_message(reply_token, Products.list_all())
    # 內用事件
    elif event.postback.data in ['here']:
        line_bot_api.reply_message(reply_token, TemplateSendMessage(alt_text="請掃描桌上的QRCODE",
                                                                    sender=Sender(
                                                                        name='服務員結衣',
                                                                        icon_url='https://i.imgur.com/S7SHmup.png'
                                                                    ),
                                                                    template=ButtonsTemplate(
                                                                        text='請掃描桌上的QRCode點餐',
                                                                        actions=[
                                                                            URIAction(
                                                                                type='uri',
                                                                                label='點我掃描',
                                                                                uri="https://liff.line.me/1654280234-Wabazm3B"
                                                                            )
                                                                        ]
                                                                    )))
    # 觸發確認訂單事件
    elif event.postback.data in ['待補', '確認訂單']:
        if cart.bucket():
            line_bot_api.reply_message(reply_token, cart.display())
        else:
            line_bot_api.reply_message(reply_token, TextSendMessage(text='你的購物車目前沒東西喔'))
    # 觸發清空購物車事件
    elif event.postback.data in ['Empty Cart']:
        cart.reset()
        line_bot_api.reply_message(reply_token, TextSendMessage(text="你的購物車已經被清空了"))
    # 如果action為check則執行結帳動作
    elif action == 'checkout':
        if not cart.bucket():
            line_bot_api.reply_message(reply_token,
                                       TextSendMessage(text='你的購物車是空的'))
            return 'OK'

        # 透過uuid來建立訂單id,它可以幫我們建立一個獨一無二的值
        order_id = uuid.uuid4().hex
        # 訂單總金額
        total = 0
        # 訂單內容物的陣列
        items = []

        for product_name, num in cart.bucket().items():
            product = db_session.query(Products).filter(Products.name.ilike(product_name)).first()

            print(product.id)
            item = Items(product_id=product.id,
                         product_name=product.name,
                         product_price=product.price,
                         order_id=order_id,
                         quantity=num)

            items.append(item)

            total += product.price * int(num)

        cart.reset()

        line_pay = LinePay()
        # 傳送這些資訊過去他會回我們一個json
        # 自己試試看把info印出來或是用postman看看裡面的結構
        info = line_pay.pay(product_name='OrderBot 點吧',
                            amount=total,
                            order_id=order_id,
                            product_image_url=Config.STORE_IMAGE_URL)

        # 從info裡面擷取付款連結跟transactionid
        pay_web_url = info['paymentUrl']['web']
        transaction_id = info['transactionId']

        # 產生訂單
        order = Orders(id=order_id,
                       transaction_id=transaction_id,
                       is_pay=False,
                       amount=total,
                       user_id=user_id)

        db_session.add(order)

        for item in items:
            db_session.add(item)

        db_session.commit()

        message = TemplateSendMessage(
            alt_text='差一點點就完成訂購囉~',
            template=ButtonsTemplate(
                text='差一點點就完成訂購囉~',
                actions=[
                    URIAction(label='Pay NT${}'.format(order.amount),
                              uri='{liff_url}?redirect_url={url}'.format(
                                  liff_url=Config.LIFF_URL,
                                  url=pay_web_url))
                ]))
        line_bot_api.reply_message(reply_token, message)

    # 訂單管理
    elif event.postback.data in ['訂單管理']:
        line_bot_api.reply_message(reply_token, Booking.list_all_user(user_id))

    # 取消訂單
    elif '取消訂位' in event.postback.data:
        line_bot_api.reply_message(reply_token, TextSendMessage(text="您的訂單已取消",
                                                                sender=Sender(
                                                                    name='會員中心管理員結衣',
                                                                    icon_url='https://i.imgur.com/S7SHmup.png'
                                                                )))
        book_id = str(event.postback.data)[4:]
        db_session.query(Booking).filter_by(id=book_id).first().is_confirm = -2
        db_session.commit()

    return 'OK'


# 當有用戶加機器人好友
@handler.add(FollowEvent)
def follow_message(event):
    # 建立用戶資料
    get_or_create_user(event.source.user_id)
    # 傳送歡迎訊息
    line_bot_api.reply_message(
        event.reply_token,
        AllMessage.welcome_message()
    )
    # 設置預設richmenu
    line_bot_api.link_rich_menu_to_user(event.source.user_id, richmenu_list.RichMenu_ID.richmenu_01)


# 如果資料庫沒找到用戶資料則建立用戶資料
def get_or_create_user(user_id):
    user = db_session.query(User).filter_by(id=user_id).first()

    if not user:
        profile = line_bot_api.get_profile(user_id)
        user = User(id=user_id,
                    user_name_origin=profile.display_name,
                    user_name_custom=profile.display_name,
                    user_image_url=profile.picture_url
                    )
        db_session.add(user)
        db_session.commit()

    return user


# 初始化產品資訊
@app.before_first_request
def init_products():
    # 判斷資料庫是否存在
    result = init_db()
    if result:
        init_data = [Products(name='芒果炒雞柳',
                              product_image_url='https://i.imgur.com/SBDmHrJ.jpg',
                              price=300,
                              description='炒雞柳好吃!'),
                     Products(name='東坡肉',
                              product_image_url='https://i.imgur.com/JCBXVEq.jpg',
                              price=310,
                              description='東坡肉好吃！'),
                     Products(name='嫩煎牛排',
                              product_image_url='https://i.imgur.com/gGhxvM6.jpg',
                              price=320,
                              description='牛排好吃！'),
                     Products(name='蒜泥白玉蒸蝦',
                              product_image_url='https://i.imgur.com/MhAb8nA.jpg',
                              price=330,
                              description='蝦子好吃！'),
                     Products(name='橙汁魚排',
                              product_image_url='https://i.imgur.com/t1svMMN.png',
                              price=290,
                              description='魚排好吃！'),
                     Products(name='蒜苗炒松阪牛',
                              product_image_url='https://i.imgur.com/JZssJkM.jpg',
                              price=340,
                              description='松阪牛好吃！')
                     ]
        db_session.bulk_save_objects(init_data)
        db_session.commit()


# 檢查手機號碼
def check_cellphone(number):
    if len(number) != 10:
        return False
    elif not re.match(r'^09\d{8}', number):
        return False
    return True


if __name__ == "__main__":
    init_products()
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_database, 'interval', seconds=60)
    scheduler.start()
    app.run()
