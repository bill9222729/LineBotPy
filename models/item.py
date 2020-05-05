from sqlalchemy import Column, DateTime, Integer, String, func, ForeignKey
from database import Base

class Items(Base):
    __tablename__ = 'items'

    #id為主鍵
    id = Column(Integer, primary_key=True)

    #產品id,名稱,價格,數量
    product_id = Column("product_id",ForeignKey("products.id"))
    product_name = Column(String)
    product_price = Column(Integer)
    quantity = Column(Integer)

    #建立時間
    created_time = Column(DateTime, default=func.now())

    #訂單id,外來鍵
    order_id = Column("order_id", ForeignKey("orders.id"))