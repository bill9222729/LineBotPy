from flask import Flask, request, abort, redirect, render_template

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

from urllib.parse import parse_qsl
import uuid

# 匯入richmenu清單
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
# 匯入linepay模組
from models.linepay import LinePay

app = Flask(__name__)

line_bot_api = LineBotApi(Config.CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(Config.CHANNEL_SECRET)

# 出大絕直接設定全域變數給付款連結
PAY_WEB_URL = ''


# 當連線中斷時自動關閉資料庫
# 資料內容來自https://flask.palletsprojects.com/en/1.1.x/patterns/sqlalchemy/
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

#LIFF的範例文件
@app.route('/index')
def index():
    #路徑不須加 templates
    return render_template(r"index.html")

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


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

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
            line_bot_api.link_rich_menu_to_user(user_id, richmenu_list.RichMenu_ID.richmenu_03)
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

        elif message_text == '待補':
            line_bot_api.reply_message(reply_token, TextSendMessage(text='cart'))


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
    if event.postback.data in ['join_us', '加入會員']:
        # 資料庫該使用者狀態改為註冊中
        # Updata data
        print('註冊中')
        query.is_signup = True
        db_session.commit()
        line_bot_api.link_rich_menu_to_user(user_id, richmenu_list.RichMenu_ID.richmenu_02)
        line_bot_api.push_message(user_id, AllMessage.sign_cellphone())
    elif event.postback.data == 'exit':
        query.is_signup = False
        query.edit_user_name = False
        query.edit_home_address = False
        query.edit_company_address = False
        db_session.commit()
        if not query.is_member:
            line_bot_api.link_rich_menu_to_user(user_id, richmenu_list.RichMenu_ID.richmenu_01)
        line_bot_api.push_message(user_id, TextSendMessage(text='好的，歡迎您再來找我聊聊天喔！'))
    elif event.postback.data == '會員中心':
        line_bot_api.push_message(user_id, TextSendMessage(text='這是專屬於你的會員中心'))
        line_bot_api.push_message(user_id, AllMessage.member_center(query))
    elif event.postback.data in ['當日外帶', 'add']:
        line_bot_api.push_message(user_id, Products.list_all())
    elif event.postback.data in ['待補', '確認訂單']:
        if cart.bucket():
            line_bot_api.reply_message(reply_token, cart.display())
        else:
            line_bot_api.reply_message(reply_token, TextSendMessage(text='你的購物車目前沒東西喔'))
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
        print('哈哈')
        print(order_id)
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
        info = line_pay.pay(product_name='linebotClient',
                            amount=total,
                            order_id=order_id,
                            product_image_url=Config.STORE_IMAGE_URL)

        # 從info裡面擷取付款連結跟transactionid
        pay_web_url = info['paymentUrl']['web']
        transaction_id = info['transactionId']

        # 把付款網址設定給全域變數
        PAY_WEB_URL = pay_web_url

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
                              description='還沒掰好'),
                     Products(name='東坡肉',
                              product_image_url='https://i.imgur.com/JCBXVEq.jpg',
                              price=310,
                              description='還沒掰好'),
                     Products(name='嫩煎牛排',
                              product_image_url='https://i.imgur.com/gGhxvM6.jpg',
                              price=320,
                              description='還沒掰好'),
                     Products(name='蒜泥白玉蒸蝦',
                              product_image_url='https://i.imgur.com/MhAb8nA.jpg',
                              price=330,
                              description='還沒掰好'),
                     Products(name='橙汁魚排',
                              product_image_url='https://i.imgur.com/ZSsqBqW.jpg',
                              price=290,
                              description='還沒掰好'),
                     Products(name='蒜苗炒松阪牛',
                              product_image_url='https://i.imgur.com/JZssJkM.jpg',
                              price=340,
                              description='還沒掰好')
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
    app.run()
