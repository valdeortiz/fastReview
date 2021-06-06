from fastapi import HTTPException
from fastapi.routing import APIRouter
from ..schemas import ReviewRequestModel, ReviewResponseModel, ReviewRequestPutModel
from ..database import User,Movie,UserReview
from typing import List

router = APIRouter(prefix='/reviews')

@router.post('', response_model=ReviewResponseModel)
async def create_review(user_review: ReviewRequestModel):

    if User.select().where(User.id == user_review.user_id).first() is None:
        raise HTTPException(status_code=404, detail='Usuario no encontrado')

    if Movie.select().where(Movie.id == user_review.movie_id).first() is None:
        raise HTTPException(status_code=404, detail='Movie no encontrado')

    user_review = UserReview.create(
        user_id=user_review.user_id,
        movie_id=user_review.movie_id,
        review=user_review.review,
        score=user_review.score
    )

    return user_review

@router.get('', response_model=List[ReviewResponseModel])
async def get_reviews(page: int = 1, limit: int = 10):
    reviews = UserReview.select().paginate(page, limit)

    return [user_review for user_review in reviews]

@router.get('/{review_id}', response_model=ReviewResponseModel)
async def get_review(review_id: int):
    review = UserReview.select().where(UserReview.id == review_id).first()
    if review is None:
        raise HTTPException(status_code=400, detail='Review no encontrado')
    
    return review



@router.put('/{review_id}', response_model=ReviewResponseModel)
async def update_review(review_id: int, review_request: ReviewRequestPutModel):
    review = UserReview.select().where(UserReview.id == review_id).first()
    if review is None:
        raise HTTPException(status_code=400, detail='Review no encontrado')

    review.review = review_request.review
    review.score = review_request.score

    review.save()
    
    return review


@router.delete('/{review_id}', response_model=ReviewResponseModel)
async def update_review(review_id: int):
    review = UserReview.select().where(UserReview.id == review_id).first()
    if review is None:
        raise HTTPException(status_code=400, detail='Review no encontrado')

    review.delete_instance()
    
    return review