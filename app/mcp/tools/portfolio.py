from sqlalchemy import select
from app.db.session import AsyncSessionLocal
from app.db.models import PortfolioItem
from app.logger import logger


def get_user_portfolio(user_id: str) -> list[dict]:
    """
    Get the user's stock portfolio from the database.
    Use this when the user asks about their portfolio, their stocks, or what they own.
    Args:
        user_id: the user's ID
    """
    import asyncio
    logger.info(f"get_user_portfolio called: user_id={user_id}")

    async def _fetch():
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(PortfolioItem).where(PortfolioItem.user_id == user_id)
            )
            items = result.scalars().all()
            return [
                {
                    "ticker": item.ticker,
                    "quantity": item.quantity,
                    "purchase_price": item.purchase_price,
                }
                for item in items
            ]

    result = asyncio.run(_fetch())
    logger.info(f"get_user_portfolio result: {len(result)} items")
    return result