#
# # 宣告背景處理
#     scheduler = BackgroundScheduler()
#     scheduler.add_job(reminder, 'interval', seconds=60)
#     scheduler.start()
from datetime import datetime

from database import db_session
from models.lineNotify import lineNotifyMessage
from models.booking import Booking
from models.user import User


def check_database():
    # 取得今日時間
    today = datetime.today()
    # 取得訂位表單內所有資料
    booking_list = db_session.query(Booking).all()
    for x in booking_list:
        # 如果日期等於今天日期
        booking_date = str(x.book_time).split(" ")[0]
        booking_time = str(x.book_time).split(" ")[1]
        booking = datetime(int(booking_date.split("-")[0]),
                           int(booking_date.split("-")[1]),
                           int(booking_date.split("-")[2]),
                           int(booking_time.split(":")[0]),
                           int(booking_time.split(":")[1]),
                           int(booking_time.split(":")[2]))
        # 如果日期差距是正的才處理
        if (booking - today).days == 1:
            query = User.query.filter_by(id=x.user_id).first()
            # 距離訂位時間十分鐘的時候提醒客人來吃飯
            if int((booking - today).seconds / 60) == 10:
                lineNotifyMessage(query.notifyToken, "\n記得你十分鐘後跟我們有訂位ㄛ！")
    return
