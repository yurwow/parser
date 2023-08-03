import requests
from bs4 import BeautifulSoup as bs
from database import add_to_database, remove_from_db_by_id, get_items_from_database
from models.product import Product
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import threading

PRODUCT_URL = "https://vladivostok.e2e4online.ru/catalog/noutbuki-42/"

app = FastAPI(title="parser",
              version="0.0.1",
              # docs_url=None,
              redoc_url=None,
              )


origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:8080",
    "http://localhost:4200",
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/get/products", tags=["fetch"])
async def fetch():
    items = get_items_from_database()
    return items
    # return await update_db()


async def update_db():
    try:
        # requests solution
        page = requests.get(url=PRODUCT_URL)
        html = page.text

        soup = bs(html, "lxml")
        items = soup.find_all("div", class_="block-offer-item subcategory-new-offers__item-block")
        products = []
        for item in items:
            title = item.find("div", class_="block-offer-item__info").find("div", class_="block-offer-item__head-info").find("a", class_="block-offer-item__name").text
            title = title.replace("\n", "")
            price = item.find("div", class_="price-block block-offer-item__price _default").find("div", class_="price-block__price _WAIT")
            price = ("".join(price.text.split()))[:-1]
            id = item.find("div", class_="block-offer-item__info").find("div", class_="block-offer-item__reference").find("div", class_="block-offer-item__reference-id").text
            id = int(id[5:])
            form = Product(id=id, title=title, price=price)
            add_to_database(form)
            json_form = {"id": id, "title": title, "price": price}
            products.append(json_form)
            print(title)
            print("price: ", price)
            print("code: ", id)
        return products
    except:
        raise HTTPException(status_code=400, detail="Couldn't update storage")


@app.post("/add")
async def add(title: str, price: int, code: int):
    try:
        form = Product(id=code, title=title, price=price)
        add_to_database(form)
    except:
        raise HTTPException(status_code=400, detail="Couldn't add product")


@app.delete("/delete")
async def delete(id: int):
    try:
        remove_from_db_by_id(id)
        return get_items_from_database()
    except:
        raise HTTPException(status_code=400, detail="Couldn't delete product from database")


@app.put("/put")
async def put(title: str, price: int, code: int):
    try:
        form = Product(id=code, title=title, price=price)
        add_to_database(form)
    except:
        raise HTTPException(status_code=400, detail="Couldn't update products info")


def update_storage():
    # Обновляем базу данных каждые 30 минут
    threading.Timer(interval=1800.0, function=update_storage).start()
    update_db()


update_storage()
# Если запуск первый, то в базе данных будут данные без необходимости ждать 30 минут
update_db()
