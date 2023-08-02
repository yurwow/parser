from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()
class Product(Base):
    __tablename__ = "price-data"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer)