from sqlalchemy import Column, String, Boolean, DateTime, func
from sqlalchemy.orm import relationship
from database import Base
import datetime


class User(Base):
    __tablename__ = 'users'

    # 用戶id(主鍵)
    id = Column(String(100), primary_key=True)
    # 用戶名稱(原始)
    user_name_origin = Column(String(100), nullable=False)
    # 用戶名稱(自訂)
    user_name_custom = Column(String(100), nullable=False)
    # 用戶大頭貼
    user_image_url = Column(String(length=256))
    # 用戶電話號碼
    phone_number = Column(String(100), nullable=True, default="還未設定電話號碼")
    # 用戶家裡地址
    home_address = Column(String(100), nullable=True, default="還未設定住家地址")
    # 用戶公司地址
    company_address = Column(String(100), nullable=True, default="還未設定公司地址")
    # 使用者資訊建立時間
    created_time = Column(DateTime(), nullable=False, default=func.now())
    # 使用者資訊最後修改時間
    created_time_final = Column(DateTime(), nullable=False, default=func.now())
    # LineNotify的token
    notifyToken = Column(String(100), nullable=True, default="")
    # 是否為會員
    is_member = Column(Boolean, nullable=False, default=False)
    # 是否在註冊中
    is_signup = Column(Boolean, nullable=False, default=False)
    # 是否正在自訂使用者名稱
    edit_user_name = Column(Boolean, nullable=False, default=False)
    # 是否正在自訂住家地址
    edit_home_address = Column(Boolean, nullable=False, default=False)
    # 是否正在自訂公司地址
    edit_company_address = Column(Boolean, nullable=False, default=False)

    # 將user與order做關聯
    orders = relationship('Orders', backref='user')

    # 以下為示意
    
    # user.orders
    # [<Order 1>, <Order 2>]

    # order.user
    # <User 1>

    # def __repr__(self):
    #     return '<User %r>' % self.id
