from  typing import List

from fastapi import APIRouter, status
from fastapi import HTTPException
from fastapi import Path

from ..schemas import AddressResponseModel
from ..schemas import AddressRequestModel
from ..schemas import AddressPutModel

from ..database import Address, User


router = APIRouter(prefix= '/address')


@router.get('/', response_model= list[AddressResponseModel])
async def get_address():
    address = Address.select()

    return [ addres for addres in address]


@router.get('/{address_id}', response_model= AddressResponseModel)
async def get_address_id(address_id: int = Path(..., title = 'Address ID', ge = 1)):
    address = Address.get_or_none((Address.id == address_id))

    if address is None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= 'Address not found')
    
    return address


@router.post('/', response_model =  AddressResponseModel)
async def create_address(address: AddressRequestModel):

    user = User.select().where(User.id == address.user.id).first()

    if user is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'User not found')

    address = Address.create(
        user = address.user.id,
        street = address.street,
        city  = address.city,
        postal_code = address.postal_code
    )

    return address


@router.put('/{id}', response_model= AddressResponseModel)
async def update_address(id:int, address_request: AddressPutModel):

    address = Address.select().where(Address.id == id).first()

    if address is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'Address not found')


    user = User.select().where(User.id == address_request.user.id).first()

    if user is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'User not found')

    address.user = address_request.user.id
    address.street = address_request.street
    address.city = address_request.city
    address.postal_code = address_request.postal_code

    address.save()

    return address



@router.delete('/{id}', response_model= AddressResponseModel)
async def delete_address(id: int):
    address = Address.select().where(Address.id == id).first()

    if address is None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= 'Address not found')

    address.delete_instance()

    return address