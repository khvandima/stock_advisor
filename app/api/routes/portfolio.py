import uuid

from fastapi import HTTPException, APIRouter, status, Depends
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.db.models import User, PortfolioItem
from app.core.dependencies import get_current_user

from app.logger import logger
from app.schemas.portfolio import PortfolioItemCreate, PortfolioItemResponse

router = APIRouter(prefix="/portfolio", tags=["portfolio"])


@router.post('/add')
async def portfolio_item_create(
        data: PortfolioItemCreate,
        current_user: User=Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
) -> PortfolioItemResponse:
    item = PortfolioItem(
        user_id=current_user.id,
        ticker=data.ticker,
        quantity=data.quantity,
        purchase_price=data.purchase_price,
    )
    try:
        db.add(item)
        await db.commit()
        await db.refresh(item)
        logger.info(f"New item added: {item.ticker}")
    except Exception as e:
        logger.error(f"Failed to add new item: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

    return PortfolioItemResponse.model_validate(item)


@router.get('/')
async def get_portfolio(
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
) -> list[PortfolioItemResponse]:

    query = select(PortfolioItem).where(PortfolioItem.user_id == current_user.id)
    result = await db.execute(query)
    items = list(result.scalars().all())
    logger.info(f"Portfolio fetched for user: {current_user.id}, items: {len(items)}")
    return items


@router.delete('/{item_id}')
async def delete_portfolio(
        item_id: uuid.UUID,
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
) -> dict:
    query = select(PortfolioItem).where(PortfolioItem.id == item_id)
    result = await db.execute(query)
    item = result.scalar_one_or_none()
    if item is None:
        logger.error(f"Portfolio item not found: {item_id}")
        raise HTTPException(status_code=404, detail="Item not found")
    if item.user_id != current_user.id:
        logger.warning(f"Unauthorized delete attempt: user {current_user.id} tried to delete item {item_id}")
        raise HTTPException(status_code=403, detail="Not permitted")
    try:
        await db.delete(item)
        await db.commit()
        logger.info(f"Portfolio item deleted: {item_id} by user {current_user.id}")
    except Exception as e:
        await db.rollback()
        logger.error(f"Failed to delete portfolio item {item_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

    return {'message': 'deleted'}