from fastapi import HTTPException
from sqlalchemy import select, ScalarResult, Executable
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.models import Product, Review


async def get_object_or_404(db: AsyncSession, query: Executable,
                            error_message: str = 'Object not found'):
    obj = await db.scalar(query)

    if obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error_message
        )

    return obj


async def get_objects_or_404(db: AsyncSession, query: Executable,
                             error_message: str = 'Object not found'):
    res: ScalarResult = await db.scalars(query)
    objs = res.all()

    if not objs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error_message
        )

    return objs


async def calculate_rating(db: AsyncSession, product: Product):
    reviews = await db.scalars(select(Review.grade).where(
        Review.product_id == product.id,
        Review.is_active == True
    ))
    all_reviews = reviews.all()
    if not all_reviews:
        new_rating = 0
    else:
        new_rating = round(sum(all_reviews) / len(all_reviews), 2)
    product.rating = new_rating
