from fastapi import FastAPI
from fastapi import APIRouter

from .database import User
from .database import Address
from .database import Review
from .database import Category
from .database import ProductCategory
from .database import Product

from .routers import user_router
from .routers import address_router
from .routers import product_router
from .routers import review_router
from .routers import category_router
from .routers import productcategory_router

from .database import database as connection

app = FastAPI()

api_v1 = APIRouter(prefix= '/api/v1')

api_v1.include_router(user_router)
api_v1.include_router(address_router)
api_v1.include_router(product_router)
api_v1.include_router(review_router)
api_v1.include_router(category_router)
api_v1.include_router(productcategory_router)

app.include_router(api_v1)


@app.on_event('startup')
def startup():
  if connection.is_closed():
      connection.connect()

  connection.create_tables([User, Product, Address, Review, Category, ProductCategory])


@app.on_event('shutdown')
def shutdown():
  if not connection.is_closed():
      connection.close()

