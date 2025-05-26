from datetime import datetime

from fastapi import APIRouter
from sqlalchemy import select, ScalarResult, insert, Sequence
from starlette import status

from app.backend.db_depends import DbSessionDep
from app.helpers.auth import CurrUserPayloadDep, user_is_customer, user_is_admin
from app.helpers.review import calculate_rating, get_object_or_404, get_objects_or_404
from app.models import Review, Product, User
from app.schemas import CreateReview

router = APIRouter(prefix="/reviews", tags=["reviews"])


@router.get("/")
async def get_all_reviews(db: DbSessionDep):
    reviews = await get_objects_or_404(
        db,
        select(Review)
        .join(Product)
        .join(User)
        .where(Review.is_active == True, Product.is_active == True, User.is_active == True),
        "There is no reviews found",
    )
    return reviews


@router.get("/{product_slug}")
async def products_reviews(db: DbSessionDep, product_slug: str):
    product: Product = await get_object_or_404(
        db, select(Product).where(Product.slug == product_slug, Product.is_active == True), "There is no product found"
    )

    reviews = await get_objects_or_404(
        db,
        select(Review).where(Review.product_id == product.id, Review.is_active == True),
        "There is no reviews for this product found",
    )
    return reviews


@router.post("/{product_slug}", status_code=status.HTTP_201_CREATED)
@user_is_customer
async def add_review(db: DbSessionDep, review: CreateReview, product_slug: str, curr_user: CurrUserPayloadDep) -> dict:
    product: Product = await get_object_or_404(
        db, select(Product).where(Product.slug == product_slug), "There is no product found"
    )

    await db.execute(
        insert(Review).values(
            user_id=curr_user.get("id"),
            product_id=product.id,
            comment=review.comment,
            grade=review.grade,
            comment_date=datetime.now(),
        )
    )

    await calculate_rating(db, product)

    await db.commit()

    return {"status_code": status.HTTP_201_CREATED, "transaction": "Review successfully created"}


@router.delete("/")
@user_is_admin
async def delete_review(db: DbSessionDep, review_id: int, curr_user: CurrUserPayloadDep) -> dict:
    review: Review = await get_object_or_404(
        db, select(Review).where(Review.id == review_id, Review.is_active == True), "There is no review found"
    )

    product: Product = await get_object_or_404(
        db, select(Product).where(Product.id == review.product_id), "There is no product found"
    )

    review.is_active = False

    await calculate_rating(db, product)

    await db.commit()

    return {"status_code": status.HTTP_200_OK, "transaction": "Review successfully deleted"}
