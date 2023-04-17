# mareety_bot_backend

mareety_bot_backend

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

License: MIT


### API эндпоинты

##### 1. `/api/v1/product-list/{category_id}/` +
##### 2. `/api/v1/product-detail/{slug}/` +
##### 3. `/api/v1/category-list/` +
##### 4. `/api/v1/cart/{customer_id}/` +
##### 5. `/api/v1/orders/{customer_id}/` +
##### 6. `/api/v1/registration/`
##### 7. `/api/v1/delete-from-cart/{product_id}/` +
##### 8. `/api/v1/change-qty-from-cart/{product_id}/` +
##### 9. `/api/v1/add-to-cart/{product_id}/` +


### Сущности:

##### 1. User
- first_name: str
- last_name: str
- phone: str
- orders (M2M-Order)
- create_at: datetime

##### 2. Product
- name: str
- slug: str
- image: str
- description: str
- price: float
- category (FK-Category)
- url: str

##### 3. Cart
- user (FK-User)
- products (M2M-Product)
- total_products: int
- final_price: float

##### 4. Category
- name: str
- slug: str
- url: str

##### 5. CartProduct
- user (FK-User)
- cart (FK-Cart)
- product (FK-Product)
- final_price: int [qty * product.price]
- qty: int

##### 6. Order
- user (FK-User)
- cart (FK-Cart)
- address: str
- create_at: datetime