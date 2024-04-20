from  typing import List

from fastapi import APIRouter, status
from fastapi import HTTPException
from fastapi import Path

from ..schemas import ProdutResponseModel
from ..schemas import ProdutRequestModel
from ..schemas import ProdutPutModel

from ..database import Product

router = APIRouter(prefix= '/product')


@router.get('/', response_model= list[ProdutResponseModel])
async def get_products(page: int = 1, limit = 10):
    product = Product.select()

    return [ produc for produc in product ]


@router.post('/', response_model= ProdutResponseModel)
async def create_product(product: ProdutRequestModel):

    product = Product.create(
        name = product.name,
        description = product.description,
        price = product.price,
        stock = product.stock
    )

    return product


@router.put('/{id}', response_model= ProdutResponseModel)
async def update_product(id: int, product_request: ProdutPutModel):
    product = Product.select().where(Product.id == id).first()

    if product is None:
        raise HTTPException(status_code= 404, detail= 'Product not found')

    product.name = product_request.name
    product.description = product_request.description
    product.price = product_request.price
    product.stock = product_request.stock

    product.save()

    return product


@router.delete('/{id}', response_model= ProdutResponseModel)
async def delete_product(id: int):
    product = Product.select().where(Product.id == id).first()

    if product is None:
        raise HTTPException(status_code= 404, detail= 'Product not found')

    product.delete_instance()

    return product
