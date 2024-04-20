from  typing import List

from fastapi import APIRouter, status
from fastapi import HTTPException
from fastapi import Path

from ..schemas import UserResponseModel
from ..schemas import UserRequestModel
from ..schemas import UserPutModel

from ..database import User


router = APIRouter(prefix= '/user')


@router.get('/', response_model= list[UserResponseModel])
async def get_user(page: int = 1, limit = 10):
    user = User.select()

    return [ usr for usr in user ]


@router.get('/{user_id}', response_model= UserResponseModel)
async def get_user_id(user_id: int = Path(..., title = 'User ID', ge = 1)):
    user = User.get_or_none((User.id == user_id))

    if user is None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= 'User not found')
    
    return user


@router.post('/', response_model= UserRequestModel)
async def create_user(user: UserRequestModel):

    user = User.create(
        username = user.username,
        email = user.email
    )

    return user


@router.put('/{id}', response_model= UserResponseModel)
async def update_user(id: int, user_request: UserPutModel):
    user = User.select().where(User.id == id).first()

    if user is None:
        raise HTTPException(status_code= 404, detail=' User not found')

    user.username = user_request.username
    user.email = user_request.email

    user.save()

    return user


@router.delete('/{id}', response_model= UserResponseModel)
async def delete_user(id: int):
    user = User.select().where(User.id == id).first()

    if user is None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= 'User not found')

    user.delete_instance()

    return user