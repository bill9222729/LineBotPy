from linebot.models import *
from sqlalchemy import Column, String, Boolean, DateTime, func, ForeignKey, Integer
from sqlalchemy.orm import relationship
from database import Base, db_session
from datetime import datetime

from library.linebot.models.send_messages import Sender
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
    def list_all_user(userid):
        booklist = db_session.query(Booking).filter_by(user_id=userid).order_by("book_time").all()
        bubbles = []
        count = 0
        for i, book in enumerate(booklist):
            # 如果沒有接受的跳過
            if book.is_confirm != 1:
                continue
            # 如果過期的跳過
            if (book.book_time - datetime.today()).days < 0:
                continue

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
                            text=str(book.book_time).split(" ")[0],
                            weight="bold",
                            size="xxl",
                            margin="md"
                        ),
                        BoxComponent(
                            layout="vertical",
                            margin="xxl",
                            spacing="sm",
                            contents=[
                                BoxComponent(
                                    layout="vertical",
                                    margin="xxl",
                                    spacing="sm",
                                    contents=[
                                        SeparatorComponent(
                                            margin="lg"
                                        ),
                                        BoxComponent(
                                            layout="horizontal",
                                            margin="xxl",
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
                                                    text=str(book.book_time).split(" ")[1],
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
                                                    text=str(book.people_num),
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
                                                    text=User.query.filter_by(id=book.user_id).first().phone_number,
                                                    size="sm",
                                                    color="#111111",
                                                    align="end"
                                                )
                                            ]
                                        ),
                                    ]
                                )],
                        ),
                        SeparatorComponent(
                            margin="xxl"
                        ),

                    ]
                ),
                footer=BoxComponent(
                    layout='vertical',
                    contents=[
                        BoxComponent(
                            layout="vertical",
                            contents=[
                                ButtonComponent(
                                    style="secondary",
                                    action=PostbackAction(
                                        label="取消訂位",
                                        text="我要取消訂位",
                                        data="取消訂位"+book.id
                                    )
                                )
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
            bubbles.append(bubble)
            count = count + 1

        if count == 0:
            print("%$%#%$#%#$%#$")
            message = TextSendMessage(text="你沒有訂單ㄛ！",
                                      sender=Sender(
                                          name='會員中心管理員結衣',
                                          icon_url='https://i.imgur.com/S7SHmup.png'
                                      ))
            return message

        carousel_container = CarouselContainer(contents=bubbles)

        message = FlexSendMessage(alt_text="預約列表",
                                  contents=carousel_container)
        return message

    @staticmethod
    def list_all_manager():
        booklist = db_session.query(Booking).order_by("book_time").all()

        bubbles = []
        sub_bubbles = []
        book_date_tmp = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        count = 0

        for i, book in enumerate(booklist):
            print("i=" + str(i) + "   len=" + str(len(booklist)))
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
            if str(book_date_tmp).split(" ")[0] != str(book.book_time).split(" ")[0]:
                print("不一樣")
                print(sub_bubbles)
                print("第哈哈" + str(i))
                if count == 0:
                    sub_bubble = add_sub_bubbles(book)
                    sub_bubbles.append(sub_bubble)
                    # 把暫存的日期改成現在這單的
                    book_date_tmp = book.book_time
                    count = count + 1
                else:
                    # 加入前一天的單
                    bubble = add_bubbles(sub_bubbles, book_date_tmp)
                    bubbles.append(bubble)
                    sub_bubbles = []
                    # 把暫存的日期改成現在這單的
                    book_date_tmp = book.book_time
                    # 加入這一天的單
                    sub_bubble = add_sub_bubbles(book)
                    sub_bubbles.append(sub_bubble)
                    count = count + 1
            else:
                print("一樣")
                print(sub_bubbles)
                sub_bubble = add_sub_bubbles(book)
                print("加入")
                sub_bubbles.append(sub_bubble)
                count = count + 1
            if i == len(booklist) - 1:
                bubble = add_bubbles(sub_bubbles, book_date_tmp)
                bubbles.append(bubble)

        print(count)
        if count == 0:
            print("%$%#%$#%#$%#$")
            message = TextSendMessage(text="你們沒有訂單ㄛ！",
                                      sender=Sender(
                                          name='會員中心管理員結衣',
                                          icon_url='https://i.imgur.com/S7SHmup.png'
                                      ))
            return message
        carousel_container = CarouselContainer(contents=bubbles)

        message = FlexSendMessage(alt_text="預約列表",
                                  contents=carousel_container)
        return message


def add_sub_bubbles(book):
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
                        text=str(book.book_time).split(" ")[1],
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
                        text=str(book.people_num),
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
                        text=User.query.filter_by(id=book.user_id).first().phone_number,
                        size="sm",
                        color="#111111",
                        align="end"
                    )
                ]
            ),
        ]
    )
    return sub_bubble


def add_bubbles(sub_bubbles, book_date_tmp):
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
                    contents=sub_bubbles,
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
