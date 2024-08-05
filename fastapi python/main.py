from fastapi import FastAPI

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



@app.get("/products")
def root():
    return products

@app.get("/products/{product_name}")
def get_product(product_name: str):
    return [product for product in products if product.get("name") == product_name]
