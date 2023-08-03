from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, declarative_base
from models.product import Product

DB_NAME = "sqlite:///db.sqlite"
ENGINE = create_engine(DB_NAME)
SESSION = Session(bind=ENGINE)
BASE = declarative_base()

with ENGINE.connect() as conn:
    # Создаем таблицу, если таковой нет
    if not conn.dialect.has_table(conn, "price-data"):
        BASE.metadata.create_all(bind=ENGINE)
        conn.execute(text('CREATE TABLE "price-data" ('
                       'id INTEGER NOT NULL, '
                       'title VARCHAR, '
                       'price INTEGER NOT NULL,'
                       'PRIMARY KEY (id));'))

def remove_from_database(item):
    SESSION.delete(item)
    SESSION.commit()


def remove_from_db_by_id(id):
    obj = SESSION.query(Product).filter_by(id=id).scalar()
    if obj is not None:
        remove_from_database(obj)


def add_to_database(item):
    remove_from_db_by_id(item.id)
    SESSION.add(item)
    SESSION.commit()


def get_items_from_database() -> [Product]:
    return SESSION.query(Product).all()
