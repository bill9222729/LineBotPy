from sqlalchemy import Column, String, Boolean, DateTime, func, ForeignKey, Integer
from sqlalchemy.orm import relationship
from database import Base
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
