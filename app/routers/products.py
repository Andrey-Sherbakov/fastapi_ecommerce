from fastapi import APIRouter, status, HTTPException
from slugify import slugify
from sqlalchemy import insert, select

from app.backend.db_depends import DbSessionDep
from app.helpers.auth import CurrUserPayloadDep, user_is_supplier
from app.helpers.review import get_objects_or_404, get_object_or_404
from app.models import Product, Category
from app.schemas import CreateProduct

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/")
async def get_all_products(db: DbSessionDep):
    products = await get_objects_or_404(
        db,
        select(Product)
        .join(Category)
        .where(
            Product.is_active == True, Category.is_active == True, Product.stock > 0
        ),
        "There are no products",
    )

    return products


@router.post("/", status_code=status.HTTP_201_CREATED)
@user_is_supplier
async def create_product(
    db: DbSessionDep, product: CreateProduct, curr_user: CurrUserPayloadDep
):
    category: Category = await get_object_or_404(
        db,
        select(Category).where(Category.id == product.category),
        "There is no such category",
    )

    await db.execute(
        insert(Product).values(
            name=product.name,
            slug=slugify(product.name),
            description=product.description,
            price=product.price,
            image_url=product.image_url,
            stock=product.stock,
            category_id=category.id,
            supplier_id=curr_user.get("id"),
        )
    )
    await db.commit()

    return {
        "status_code": status.HTTP_201_CREATED,
        "transaction": "Product successfully created",
    }


@router.get("/{category_slug}")
async def product_by_category(db: DbSessionDep, category_slug: str):
    category: Category = await get_object_or_404(
        db,
        select(Category).where(
            Category.slug == category_slug, Category.is_active == True
        ),
        "There is no such category",
    )

    subcategories = await db.scalars(
        select(Category).where(
            Category.parent_id == category.id, Category.is_active == True
        )
    )

    cat_ids = [category.id] + [cat.id for cat in subcategories.all()]

    products = await db.scalars(
        select(Product).where(
            Product.category_id.in_(cat_ids),
            Product.is_active == True,
            Product.stock > 0,
        )
    )

    return products.all()


@router.get("/detail/{product_slug}")
async def product_detail(db: DbSessionDep, product_slug: str):
    product: Product = await get_object_or_404(
        db,
        select(Product).where(
            Product.slug == product_slug,
            Product.is_active == True,
            Product.stock > 0,
        ),
        "There is no product found",
    )

    return product


@router.put("/{product_slug}")
@user_is_supplier
async def update_product(
    db: DbSessionDep,
    product_slug: str,
    new_product: CreateProduct,
    curr_user: CurrUserPayloadDep,
):
    product: Product = await get_object_or_404(
        db,
        select(Product).where(Product.slug == product_slug),
        "There is no product found",
    )

    if product.supplier_id != curr_user.get("id"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to use this method",
        )

    category = await get_object_or_404(
        db,
        select(Category).where(
            Category.slug == new_product.category, Category.is_active == True
        ),
        "There is no such category",
    )

    product.name = (new_product.name,)
    product.slug = (slugify(new_product.name),)
    product.description = (new_product.description,)
    product.price = (new_product.price,)
    product.image_url = (new_product.image_url,)
    product.stock = (new_product.stock,)
    product.category_id = (category.id,)

    await db.commit()

    return {
        "status_code": status.HTTP_200_OK,
        "transaction": "Product update is successful",
    }


@router.delete("/{product_slug}")
@user_is_supplier
async def delete_product(
    db: DbSessionDep, product_slug: str, curr_user: CurrUserPayloadDep
):
    product = await get_object_or_404(
        db,
        select(Product).where(Product.slug == product_slug, Product.is_active == True),
        "There is no product found",
    )

    if product.supplier_id != curr_user.get("id"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to use this method",
        )

    product.is_active = False

    await db.commit()

    return {
        "status_code": status.HTTP_200_OK,
        "transaction": "Category delete is successful",
    }
