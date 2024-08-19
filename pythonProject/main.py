from fastapi import FastAPI, HTTPException, Query
from typing import List, Optional

app = FastAPI()

products = [
    {"id": 1, "name": "Samsung", "version": "S23 Ultra", "price": 1200, "category": "telephone"},
    {"id": 2, "name": "iPhone", "version": "15Pro", "price": 1300, "category": "telephone"},
    {"id": 3, "name": "Xiaomi", "version": "Note 12", "price": 900, "category": "telephone"},
    {"id": 4, "name": "Samsung", "version": "zflip 5", "price": 1150, "category": "telephone"},
    {"id": 5, "name": "iPhone", "version": "14Pro Max", "price": 1200, "category": "telephone"},
    {"id": 6, "name": "Hp", "version": "Victus", "price": 13000, "category": "Laptop"},
    {"id": 7, "name": "Asus", "price": 11000, "category": "Laptop"},
    {"id": 8, "name": "Acer", "price": 10500, "category": "Laptop"},
    {"id": 9, "name": "Samsung", "version": "Galaxy book pro2", "price": 20000, "category": "Laptop"},
    {"id": 10, "name": "Apple", "version": "Macbook air m3", "price": 30000, "category": "Laptop"},
    {"id": 11, "name": "Hp", "version": "Pavilion", "price": 19000, "category": "Laptop"}
]

@app.get("/")
def root():
    return {"message": "Главная страница"}

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


@app.get("/products")
def get_products_limit(limit: int):
    return products[:limit]

@app.get("/products/asc")
def get_products_ascending():
    sorted_products = sorted(products, key=lambda product: product["price"])
    return sorted_products

@app.get("/products/desc")
def get_products_sorted_by_price_desc():
    sorted_products = sorted(products, key=lambda product: product["price"], reverse=True)
    return sorted_products

@app.get("/search")
def search_products(
    category: Optional[str] = None,
    min_price: Optional[int] = None,
    max_price: Optional[int] = None,
    sort_by_price: Optional[str] = None,
    limit: Optional[int] = Query (10, gt=0)
):

    filtered_products = [product for product in products if category is None or product["category"] == category]

 
    filtered_products = [
        product for product in filtered_products
        if (min_price is None or product["price"] >= min_price) and
           (max_price is None or product["price"] <= max_price)
    ]

    
    if sort_by_price == "asc":
        filtered_products.sort(key=lambda product: product["price"])
    elif sort_by_price == "desc":
        filtered_products.sort(key=lambda product: product["price"], reverse=True)

    
    return filtered_products[:limit]
