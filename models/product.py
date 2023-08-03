from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()
class Product(Base):
    __tablename__ = "price-data"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    price = Column(Integer)