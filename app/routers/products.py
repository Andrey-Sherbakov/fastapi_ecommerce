from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from slugify import slugify
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.db_depends import get_db
from app.models import Product, Category
from app.schemas import CreateProduct

router = APIRouter(prefix='/products', tags=['products'])


@router.get('/')
async def get_all_products(db: Annotated[AsyncSession, Depends(get_db)]):
    products = await db.scalars(select(Product).join(Category).where(
        Product.is_active == True,
        Category.is_active == True,
        Product.stock > 0
    ))
    all_products = products.all()

    if not all_products:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There are no products'
        )

    return all_products


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_product(db: Annotated[AsyncSession, Depends(get_db)], product: CreateProduct):
    category = await db.scalar(select(Category).where(Category.id == product.category))
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There is no such category'
        )

    await db.execute(insert(Product).values(
        name=product.name,
        slug=slugify(product.name),
        description=product.description,
        price=product.price,
        image_url=product.image_url,
        stock=product.stock,
        category_id=product.category,
    ))
    await db.commit()

    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Product successfully created'
    }


@router.get('/{category_slug}')
async def product_by_category(db: Annotated[AsyncSession, Depends(get_db)], category_slug: str):
    category = await db.scalar(select(Category).where(Category.slug == category_slug, Category.is_active == True))

    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There is no such category'
        )

    subcategories = await db.scalars(select(Category).where(
        Category.parent_id == category.id,
        Category.is_active == True
    ))

    cat_ids = [category.id] + [cat.id for cat in subcategories.all()]

    products = await db.scalars(select(Product).where(
        Product.category_id.in_(cat_ids),
        Product.is_active == True,
        Product.stock > 0
    ))

    return products.all()


@router.get('/detail/{product_slug}')
async def product_detail(db: Annotated[AsyncSession, Depends(get_db)], product_slug: str):
    product = await db.scalar(select(Product).where(
        Product.slug == product_slug,
        Product.is_active == True,
        Product.stock > 0,
    ))

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There is no product found'
        )

    return product


@router.put('/{product_slug}')
async def update_product(db: Annotated[AsyncSession, Depends(get_db)], product_slug: str, new_product: CreateProduct):
    product = await db.scalar(select(Product).where(Product.slug == product_slug))
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There is no product found'
        )

    category = await db.scalar(select(Category).where(
        Category.slug == new_product.category,
        Category.is_active == True
    ))
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There is no such category'
        )

    product.name = new_product.name,
    product.slug = slugify(new_product.name),
    product.description = new_product.description,
    product.price = new_product.price,
    product.image_url = new_product.image_url,
    product.stock = new_product.stock,
    product.category_id = new_product.category,

    await db.commit()

    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Product update is successful'
    }


@router.delete('/{product_slug}')
async def delete_product(db: Annotated[AsyncSession, Depends(get_db)], product_slug: str):
    product = await db.scalar(select(Product).where(Product.slug == product_slug, Product.is_active == True))
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There is no product found'
        )

    product.is_active = False

    await db.commit()

    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Category delete is successful'
    }
