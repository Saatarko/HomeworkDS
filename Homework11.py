from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, DateTime, func
from sqlalchemy.orm import declarative_base, Session, relationship
from datetime import datetime, timezone

Base = declarative_base()

class Goods(Base):
    __tablename__ = 'goods'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    purchase = relationship("Purchase", back_populates="goods")
    delivery = relationship("Delivery", back_populates="goods")

class Sellers(Base):
    __tablename__ = 'sellers'
    
    id = Column(Integer, primary_key=True)
    name_sellers = Column(String, nullable=False)

    delivery = relationship("Delivery", back_populates="seller")

class Buyers(Base):
    __tablename__ = 'buyers'
    
    id = Column(Integer, primary_key=True)
    name_buyer = Column(String, nullable=False)

    purchase = relationship("Purchase", back_populates="buyers")

class Purchase(Base):
    __tablename__ = 'purchase'
    
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, default=lambda: datetime.now(timezone.utc))  # Автоматически подставляет текущую дату
    buyers_id = Column(Integer, ForeignKey('buyers.id'))
    goods_id = Column(Integer, ForeignKey('goods.id'))
    quantity = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)

    buyers = relationship("Buyers", back_populates="purchase")
    goods = relationship("Goods", back_populates="purchase")

class Delivery(Base):
    __tablename__ = 'delivery'
    
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, default=lambda: datetime.now(timezone.utc))  # Автоматическая текущая дата
    sellers_id = Column(Integer, ForeignKey('sellers.id'))
    goods_id = Column(Integer, ForeignKey('goods.id'))
    quantity = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)

    seller = relationship("Sellers", back_populates="delivery")
    goods = relationship("Goods", back_populates="delivery")

class Warehouse(Base):
    __tablename__ = 'warehouse'
    
    id = Column(Integer, primary_key=True)
    goods_id = Column(Integer, ForeignKey('goods.id'))
    quantity = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)


# Создаем соединение с базой данных
engine = create_engine("sqlite:///content/mybase.db")


