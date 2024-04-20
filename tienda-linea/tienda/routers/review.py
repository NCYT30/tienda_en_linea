from  typing import List

from fastapi import APIRouter, status
from fastapi import HTTPException
from fastapi import Path

from ..schemas import ReviewResponseModel
from ..schemas import ReviewRequestModel
from ..schemas import ReviewPutModel

from ..database import Review, User, Product

router = APIRouter(prefix= '/review')


@router.get('/', response_model= list[ReviewResponseModel])
async def get_review(page: int = 1, limit = 10):
    review = Review.select()

    return [ rev for rev in review ]


@router.post('/', response_model= ReviewResponseModel)
async def create_review(review: ReviewRequestModel):

    user = User.select(User.id == review.user_id.id).first()

    product = Product.select(Product.id == review.product_id.id).first()

    if user is None:
        raise HTTPException(status_code= 404, detail= 'User not found')

    if product is None:
        raise HTTPException(status_code= 404, detail= 'Product not found')

    review = Review.create(
        user_id = review.user_id.id,
        product_id = review.product_id.id,
        rating = review.rating,
        comment = review.comment
    )

    return review


@router.put('/{id}', response_model= ReviewResponseModel)
async def update_review(id: int, review_request: ReviewPutModel):
    review = Review.select().where(Review.id == id).first()

    if review is None:
        raise HTTPException(status_code= 404, detail= 'Review not found')

    review.user_id = review_request.user_id.id
    review.product_id = review_request.product_id.id
    review.rating = review_request.rating
    review.comment = review_request.comment

    review.save()

    return review




@router.delete('/{id}', response_model= ReviewResponseModel)
async def delete_review(id: int):
    review = Review.select().where(Review.id == id).first()

    if review is None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= 'Review not found')

    review.delete_instance()

    return review