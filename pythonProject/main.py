from fastapi import FastAPI, HTTPException, Query
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
from fastapi import requests
from typing import List


app = FastAPI()

products = [
    {"id": 1, "name": "Samsung", "version": "S23 Ultra", "price": 1200, "category": "telephone", "is_new": True, "discount": 15, "discount_end_date": "2024-09-10"},
    {"id": 2, "name": "iPhone", "version": "15Pro", "price": 1300, "category": "telephone", "is_new": True, "discount": 5, "discount_end_date": None},
    {"id": 3, "name": "Xiaomi", "version": "Note 12", "price": 900, "category": "telephone", "is_new": False, "discount": None, "discount_end_date": None},
    {"id": 4, "name": "Samsung", "version": "zflip 5", "price": 1150, "category": "telephone", "is_new": True, "discount": 5, "discount_end_date": "2024-09-15"},
    {"id": 5, "name": "iPhone", "version": "14Pro Max", "price": 1200, "category": "telephone", "is_new": True, "discount": 5,"discount_end_date": "2024-08-10"},
    {"id": 6, "name": "Hp", "version": "Victus", "price": 13000, "category": "Laptop", "is_new": False, "discount": 25, "discount_end_date": "2024-09-15"},
    {"id": 7, "name": "Asus", "price": 11000, "category": "Laptop", "is_new": False, "discount": 15, "discount_end_date": "2024-09-10"},
    {"id": 8, "name": "Acer", "price": 10500, "category": "Laptop", "is_new": False, "discount": 20, "discount_end_date": "2024-08-29"},
    {"id": 9, "name": "Samsung", "version": "Galaxy book pro2", "price": 20000, "category": "Laptop", "is_new": True, "discount": 15, "discount_end_date": "2024-09-20"},
    {"id": 10, "name": "Apple", "version": "Macbook air m3", "price": 30000, "category": "Laptop", "is_new": True, "discount": 50, "discount_end_date": "2024-08-27"},
    {"id": 11, "name": "Hp", "version": "Pavilion", "price": 19000, "category": "Laptop", "is_new": True, "discount": None, "discount_end_date": None}
]

@app.get("/")
def root():
    return {"message": "Главная страница"}

@app.get("/products")
def root():
    return products


@app.get("/product/{product_id}")
def get_product(product_id: int):
    product = next((p for p in products if p.get("id") == product_id), None)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.get("/products/category/{product_category}")
def get_products_by_category(product_category: str):
    filtered_products = [product for product in products if product.get("category") == product_category]
    if not filtered_products:
        raise HTTPException(status_code=404, detail="No products found in this category")
    return filtered_products

@app.get("/products-by-price")
def get_products_by_price(min_price: Optional[int] = None, max_price: Optional[int] = None):
    filtered_products = [
        product for product in products
        if (min_price is None or product["price"] >= min_price) and
           (max_price is None or product["price"] <= max_price)
    ]
    return filtered_products

@app.get("/categories")
def get_categories():

    categories = list(set(product['category'] for product in products))
    return {"categories": categories}

@app.get("/products/asc")
def get_products_ascending():
    sorted_products = sorted(products, key=lambda product: product["price"])
    return sorted_products

@app.get("/products/desc")
def get_products_sorted_by_price_desc():
    sorted_products = sorted(products, key=lambda product: product["price"], reverse=True)
    return sorted_products

@app.get("/productsnew")
def get_products_new(is_new: Optional[bool] = None):
    if is_new is not None:
        filtered_products = [product for product in products if product["is_new"] == is_new]
    return filtered_products


@app.get("/discounted-products")
def get_discounted_products():
    today = datetime.today().strftime('%Y-%m-%d')
    discounted_products = [
        product for product in products
        if product.get("discount") is not None and 
           product.get("discount_end_date") is not None and 
           product["discount_end_date"] >= today
    ]

    return discounted_products

cart = []

class CartItem(BaseModel):
    customer_id: int       
    product_id: int        
    quantity: int          
    date_added: Optional[datetime] = None 
    


@app.post("/cart/")
def add_item_to_cart(item: CartItem):
    item.date_added = datetime.utcnow()
    cart.append(item)
    return {"message": "Товар добавлен в корзину", "item": item}\
    
@app.get("/cart")
def get_cart_items():
    if not cart:  
        return {"message": "Корзина пуста"}

    quantity = sum(item.quantity for item in cart)  
    price = sum(item.quantity * next((p['price'] for p in products if p['id'] == item.product_id), 0) for item in cart)

    return {
        "items": cart,
        "quantity": quantity,
        "price": price
    }


@app.delete("/cart")
def clear_cart():
    cart.clear()
    return {"message": "Корзина очищена"}

class NewsItem(BaseModel):
    id: int
    title: str
    description: str
    images: List[str]
    category: str


news = [
    {
        "id": 1,
        "title": "Новая модель iPhone",
        "description": "Apple представила новую модель iPhone c улучшенной камерой и батареей.",
        "images": [
            "https://example.com/images/iphone1.jpg",
            "https://example.com/images/iphone2.jpg",
            "https://example.com/images/iphone3.jpg",
            "https://example.com/images/iphone4.jpg",
            "https://example.com/images/iphone5.jpg",
            "https://example.com/images/iphone6.jpg"
        ],
        "category": "Technology"
    },
    {
        "id": 2,
        "title": "Samsung Galaxy Fold",
        "description": "Samsung анонсировал новый складной телефон c гибким экраном.",
        "images": [
            "https://example.com/images/galaxy_fold1.jpg",
            "https://example.com/images/galaxy_fold2.jpg",
            "https://example.com/images/galaxy_fold3.jpg",
            "https://example.com/images/galaxy_fold4.jpg",
            "https://example.com/images/galaxy_fold5.jpg",
            "https://example.com/images/galaxy_fold6.jpg"
        ],
        "category": "Technology"
    },
    {
        "id": 3,
        "title": "Политические события",
        "description": "Последние новости o международных политических событиях.",
        "images": [
            "https://example.com/images/politics1.jpg",
            "https://example.com/images/politics2.jpg",
            "https://example.com/images/politics3.jpg",
            "https://example.com/images/politics4.jpg",
            "https://example.com/images/politics5.jpg",
            "https://example.com/images/politics6.jpg"
        ],
        "category": "Politics"
    }
]


@app.get("/news", response_model=List[NewsItem])
def get_news():
    if not news:
        return {"message": "Новостей нет"}
    return news

@app.get("/news/category/{category}", response_model=List[NewsItem])
def get_news_by_category(category: str):
    filtered_news = [item for item in news if item["category"].lower() == category.lower()]
    return filtered_news