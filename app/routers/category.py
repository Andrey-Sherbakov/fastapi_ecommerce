from fastapi import APIRouter
from fastapi import status
from slugify import slugify
from sqlalchemy import insert, select

from app.backend.db_depends import DbSessionDep
from app.helpers.auth import CurrUserPayloadDep, user_is_admin
from app.helpers.review import get_object_or_404
from app.models import Category
from app.schemas import CreateCategory

router = APIRouter(prefix="/categories", tags=["category"])


@router.get("/")
async def get_all_categories(db: DbSessionDep):
    categories = await db.scalars(select(Category).where(Category.is_active == True))
    return categories.all()


@router.post("/", status_code=status.HTTP_201_CREATED)
@user_is_admin
async def create_category(
    db: DbSessionDep, category: CreateCategory, curr_user: CurrUserPayloadDep
):
    await db.execute(
        insert(Category).values(
            name=category.name, parent_id=category.parent_id, slug=slugify(category.name)
        )
    )

    await db.rollback()

    return {"status_code": status.HTTP_201_CREATED, "transaction": "Successful"}


@router.put("/{category_slug}")
@user_is_admin
async def update_category(
    db: DbSessionDep,
    category_slug: str,
    update_category: CreateCategory,
    curr_user: CurrUserPayloadDep,
):
    category: Category = await get_object_or_404(
        db, select(Category).where(Category.slug == category_slug), "There is no such category"
    )

    category.name = update_category.name
    category.slug = slugify(update_category.name)
    category.parent_id = update_category.parent_id

    await db.commit()

    return {"status_code": status.HTTP_200_OK, "transaction": "Category update is successful"}


@router.delete("/{category_slug}")
@user_is_admin
async def delete_category(db: DbSessionDep, category_slug: str, curr_user: CurrUserPayloadDep):
    category = await get_object_or_404(
        db,
        select(Category).where(Category.slug == category_slug, Category.is_active == True),
        "There is no such category",
    )

    category.is_active = False

    await db.commit()

    return {"status_code": status.HTTP_200_OK, "transaction": "Category delete is successful"}
