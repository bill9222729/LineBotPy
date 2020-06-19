from linebot.models import *
from sqlalchemy import Column, String, Boolean, DateTime, func, ForeignKey, Integer
from sqlalchemy.orm import relationship
from database import Base, db_session
from datetime import datetime

from models.user import User


class Booking(Base):
    __tablename__ = 'booking'

    # 訂單編號(主鍵)
    id = Column(String(100), primary_key=True)
    # 訂位時間
    book_time = Column(DateTime, default=func.now())
    # 是否允許
    is_confirm = Column(Integer, default=0)
    # 預約人數
    people_num = Column(Integer)
    # user.id(外來鍵)
    user_id = Column("user_id", ForeignKey("users.id"))

    @staticmethod
    def list_all():
        booklist = db_session.query(Booking).order_by("book_time").all()

        bubbles = []
        sub_bubbles = []
        book_date_tmp = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        sub_bubble = 123
        is_first = True
        count = 1

        for book in booklist:
            print("﹀﹀﹀﹀﹀﹀")
            print(book_date_tmp)
            print(book.book_time)
            print("距離時間：")
            print((book.book_time - datetime.today()).days)
            print("︿︿︿︿︿︿")
            # 如果沒有接受的跳過
            if book.is_confirm != 1:
                continue
            # 如果過期的跳過
            if (book.book_time - datetime.today()).days < 0:
                continue
            # 如果日期有變化就就把同一日期的加入同一張表單
            if book_date_tmp != book.book_time:
                print("不一樣")
                if is_first:
                    book_date_tmp = book.book_time
                    sub_bubble = add_sub_bubbles(book, book_date_tmp)
                    print("加入")
                    sub_bubbles.append(sub_bubble)
                    is_first = False
                else:
                    print("第哈哈" + str(count))
                    # 先設置一個變數儲存當前日期
                    book_date_tmp = book.book_time
                    # 把目前的內容塞進同一張單
                    bubble = add_bubbles(sub_bubble, book_date_tmp)
                    bubbles.append(bubble)
            else:
                print("一樣")
                sub_bubble = add_sub_bubbles(book, book_date_tmp)
                print("加入")
                sub_bubbles.append(sub_bubble)
            count = count + 1
            if count > len(booklist):
                bubble = add_bubbles(sub_bubble, book_date_tmp)
                bubbles.append(bubble)

        carousel_container = CarouselContainer(contents=bubbles)

        message = FlexSendMessage(alt_text="預約列表",
                                  contents=carousel_container)
        return message


def add_sub_bubbles(book, book_date_tmp):
    sub_bubble = BoxComponent(
        layout="vertical",
        margin="xxl",
        spacing="sm",
        contents=[
            SeparatorComponent(),
            BoxComponent(
                layout="horizontal",
                contents=[
                    TextComponent(
                        text="名稱：",
                        size="sm",
                        color="#555555",
                        flex=0
                    ),
                    TextComponent(
                        text=User.query.filter_by(id=book.user_id).first().user_name_custom,
                        size="sm",
                        color="#111111",
                        align="end"
                    )
                ]
            ),
            BoxComponent(
                layout="horizontal",
                contents=[
                    TextComponent(
                        text="預約時間：",
                        size="sm",
                        color="#555555",
                        flex=0
                    ),
                    TextComponent(
                        text=str(book_date_tmp).split(" ")[1],
                        size="sm",
                        color="#111111",
                        align="end"
                    )
                ]
            ),
            BoxComponent(
                layout="horizontal",
                contents=[
                    TextComponent(
                        text="預約人數：",
                        size="sm",
                        color="#555555",
                        flex=0
                    ),
                    TextComponent(
                        text="1",
                        size="sm",
                        color="#111111",
                        align="end"
                    )
                ]
            ),
            BoxComponent(
                layout="horizontal",
                contents=[
                    TextComponent(
                        text="連絡電話",
                        size="sm",
                        color="#555555",
                        flex=0
                    ),
                    TextComponent(
                        text="0928012729",
                        size="sm",
                        color="#111111",
                        align="end"
                    )
                ]
            ),
        ]
    )
    return sub_bubble


def add_bubbles(sub_bubble, book_date_tmp):
    bubble = BubbleContainer(
        body=BoxComponent(
            layout='vertical',
            contents=[
                TextComponent(
                    text="預約清單",
                    weight="bold",
                    color='#1DB446',
                    size="sm"
                ),
                TextComponent(
                    text=str(book_date_tmp).split(" ")[0],
                    weight="bold",
                    size="xxl",
                    margin="md"
                ),
                BoxComponent(
                    layout="vertical",
                    margin="xxl",
                    spacing="sm",
                    contents=[
                        SeparatorComponent(),
                        sub_bubble,
                    ]
                ),
                SeparatorComponent(),
                BoxComponent(
                    layout="horizontal",
                    margin="md",
                    contents=[
                        TextComponent(
                            text="Created by",
                            size="xs",
                            color="#aaaaaa",
                            flex=0
                        ),
                        TextComponent(
                            text="AI戰神",
                            color="#aaaaaa",
                            size="xs",
                            align="end"
                        )
                    ]
                )
            ]
        ),
        styles=BubbleStyle(
            footer=BubbleStyle(
                separator=True
            )
        )
    )

    return bubble
