from typing import Any

from datetime import date

from pydantic import BaseModel

from pydantic.utils import GetterDict

from peewee import ModelSelect

from decimal import Decimal

class PeeWeeGetterDict(GetterDict):
    def get(self, key: Any, default: Any = None):

        res = getattr(self._obj, key, default)
        if isinstance(res, ModelSelect):
            return list(res)
        
        return res 


class ResponseModel(BaseModel):

    class Config:
        orm_mode = True
        getter_dict = PeeWeeGetterDict


#---------User-------------

class UserResponseModel(ResponseModel):
    id: int
    username: str
    email: str


class UserRequestModel(BaseModel):
    username: str
    email: str


class UserPutModel(BaseModel):
    username: str
    email: str


#--------Address-----------

class AddressResponseModel(ResponseModel):
    id: int
    user: UserResponseModel
    street: str
    city: str
    postal_code: str


class AddressRequestModel(BaseModel):
    user: UserResponseModel
    street: str
    city: str
    postal_code: str


class AddressPutModel(BaseModel):
    user: UserResponseModel
    street: str
    city: str
    postal_code: str


#----------Product------------


class ProdutResponseModel(ResponseModel):
    id: int
    name: str
    description: str
    price: Decimal
    stock: int


class ProdutRequestModel(ResponseModel):
    name: str
    description: str
    price: Decimal
    stock: int
    

class ProdutPutModel(ResponseModel):
    name: str
    description: str
    price: Decimal
    stock: int
    


#--------Review-------------


class ReviewResponseModel(ResponseModel):
    id: int
    product_id: ProdutResponseModel
    user_id: UserResponseModel
    rating: int
    comment: str


class ReviewRequestModel(BaseModel):
    product_id: ProdutResponseModel
    user_id: UserResponseModel
    rating: int
    comment: str


class ReviewPutModel(BaseModel):
    product_id: ProdutResponseModel
    user_id: UserResponseModel
    rating: int
    comment: str


#----------Category---------


class CategoryResponseModel(ResponseModel):
    id: int
    name: str
    description: str


class CategoryRequestModel(BaseModel):
    name: str
    description: str


class CategoryPutModel(BaseModel):
    name: str
    description: str


#------------ProductCategory--------------


class ProductCategoryResponseModel(ResponseModel):
    id: int
    product: ProdutResponseModel
    category: CategoryResponseModel


class ProductCategoryRequestModel(ResponseModel):
    product: ProdutResponseModel
    category: CategoryResponseModel


class ProductCategoryPutModel(ResponseModel):
    product: ProdutResponseModel
    category: CategoryResponseModel


