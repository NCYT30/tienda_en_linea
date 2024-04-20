from  typing import List

from fastapi import APIRouter, status
from fastapi import HTTPException
from fastapi import Path

from ..schemas import ProductCategoryResponseModel
from ..schemas import ProductCategoryRequestModel
from ..schemas import ProdutPutModel

from ..database import ProductCategory, Product, Category


router = APIRouter(prefix= '/productcategory')


@router.get('/', response_model= list[ProductCategoryResponseModel])
async def get_productcategory(page: int = 1, limit = 10):
    proca = ProductCategory.select()

    return [ pro for pro in proca ]


@router.post('/', response_model=ProductCategoryResponseModel)
async def create_productcategory(proca: ProductCategoryRequestModel):

    product = Product.select().where(Product.id == proca.product.id).first()

    category = Category.select().where(Category.id == proca.category.id).first()

    if product is None:
        raise HTTPException(status_code=404, detail='Product not found')
    
    if category is None:
        raise HTTPException(status_code=404, detail='Category not found')

    
    proca = ProductCategory.create(
        product=proca.product.id,
        category=proca.category.id
    )

    return proca


@router.put('/{id}', response_model=ProductCategoryResponseModel)
async def update_productcategory(id: int, proca: ProdutPutModel):

    product_category = ProductCategory.get_or_none(id=id)

    if product_category is None:
        raise HTTPException(status_code=404, detail='Product Category not found')

    product = Product.select().where(Product.id == proca.product.id).first()
    category = Category.select().where(Category.id == proca.category.id).first()

    if product is None:
        raise HTTPException(status_code=404, detail='Product not found')
    
    if category is None:
        raise HTTPException(status_code=404, detail='Category not found')

    product_category.product = proca.product.id
    product_category.category = proca.category.id
    product_category.save()

    return product_category


@router.delete('/{id}', response_model=ProductCategoryResponseModel)
async def delete_productcategory(id: int):

    product_category = ProductCategory.get_or_none(id=id)

    if product_category is None:
        raise HTTPException(status_code=404, detail='Product Category not found')

    product_category.delete_instance()

    return product_category
