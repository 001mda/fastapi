from fastapi import FastAPI, HTTPException, Query
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
from fastapi import requests


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
    return {"message": "Товар добавлен в корзину", "item": item}

@app.get("/cart", response_model=List[CartItem])
def get_cart_items():
     return cart

@app.delete("/cart")
def clear_cart():
    cart.clear()
    return {"message": "Корзина очищена"}