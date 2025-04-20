from fastapi import APIRouter

router = APIRouter(prefix='/categories', tags=['category'])


@router.get('/')
async def get_all_categories():
    pass


@router.post('/')
async def create_category():
    pass


@router.get('/{category_id}')
async def get_category():
    pass


@router.put('/{category_id}')
async def update_category():
    pass


@router.delete('/{category_id}')
async def delete_category():
    pass