from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base
from models.product import Product

DB_NAME = "sqlite:///db.sqlite"
engine = create_engine(DB_NAME)
session = Session(bind=engine)
BASE = declarative_base()

with engine.connect() as conn:
    # Создаем таблицу, если таковой нет
    if not conn.dialect.has_table(conn, "price"):
        BASE.metadata.create_all(bind=engine)

def remove_from_db(item):
    session.delete(item)
    session.commit()

def remove_by_id(id):
    obj = session.query(Product).filter_by(id=id).scalar()
    if obj is not None:
        remove_from_db(obj)

def add_to_db(item):
    remove_by_id(item.id)
    session.add(item)
    session.commit()

def fetch_from_db() -> [Product]:
    return session.query(Product).all()
