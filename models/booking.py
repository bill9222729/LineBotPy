from linebot.models import *
from sqlalchemy import Column, String, Boolean, DateTime, func, ForeignKey, Integer
from sqlalchemy.orm import relationship
from database import Base, db_session
import datetime

class Booking(Base):
    __tablename__ = 'booking'

    # 訂單編號(主鍵)
    id = Column(String(100), primary_key=True)
    # 訂位時間
    book_time = Column(DateTime, default=func.now())
    # 是否允許
    is_confirm = Column(Integer, default=0)
    # user.id(外來鍵)
    user_id = Column("user_id", ForeignKey("users.id"))

    @staticmethod
    def list_all():
        booklist = db_session.query(Booking).all()

        bubbles = []

        for book in booklist:
            if book.is_confirm != 0:
                continue

            print(type(book.book_time))
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
                            text="訂單日期",
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
                                            text="陳又玄",
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
                                            text="13:05",
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

            carousel_container = CarouselContainer(contents=bubbles)

            message = FlexSendMessage(alt_text="預約列表",
                                      contents=carousel_container)

        return message
