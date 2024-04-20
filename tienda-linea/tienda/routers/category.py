from  typing import List

from fastapi import APIRouter, status
from fastapi import HTTPException
from fastapi import Path

from ..schemas import CategoryResponseModel
from ..schemas import CategoryRequestModel
from ..schemas import CategoryPutModel

from ..database import Category

router = APIRouter(prefix= '/category')


@router.get('/', response_model= list[CategoryResponseModel])
async def get_category(page: int = 1, limit = 10):
    category = Category.select()

    return [ cat for cat in category ]


@router.post('/', response_model= CategoryResponseModel)
async def create_category(category: CategoryRequestModel):

    category = Category.create(
        name = category.name,
        description = category.description
    )

    return category


@router.put('/{id}', response_model= CategoryResponseModel)
async def update_category(id: int, category_request: CategoryPutModel):
    category = Category.select().where(Category.id == id).first()

    if category is None:
        raise HTTPException(status_code= 404, detail= 'Category not found')
    

    category.name = category_request.name
    category.description = category_request.description

    category.save()

    return category


@router.delete('/{id}', response_model= CategoryResponseModel)
async def delete_category(id: int):
    category = Category.select().where(Category.id == id).first()

    if category is None:
        raise HTTPException(status_code= 404, detail= 'Category not found')

    
    category.delete_instance()

    return category