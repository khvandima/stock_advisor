from sqlalchemy import select
from app.db.session import AsyncSessionLocal
from app.db.models import User, PortfolioItem, Digest, Alert

from langchain_core.messages import HumanMessage

from app.agent.graph import llm

from app.mcp.tools.krx_data import get_stock_price
from app.mcp.tools.signals import get_signal
from app.mcp.tools.tavily_news import tavily_search

from app.logger import logger


async def generate_digest_for_user(user: User, session) -> str:
    query = select(PortfolioItem).where(PortfolioItem.user_id == user.id)
    result = await session.execute(query)
    items = list(result.scalars().all())
    if not items:
        logger.info(f"Empty portfolio for user: {user.id}, skipping")
        return None
    logger.info(f"Portfolio fetched for user: {user.id}, items: {len(items)}")
    portfolio_data = []
    for item in items:
        try:
            price_data = get_stock_price(item.ticker)
            signal_data = get_signal(item.ticker)
            news_data = tavily_search(f"{item.ticker} 주식 뉴스")
            portfolio_data.append({
                "ticker": item.ticker,
                "quantity": item.quantity,
                "purchase_price": item.purchase_price,
                "current_price": price_data,
                "signal": signal_data,
                "news": news_data,
            })
        except Exception as e:
            logger.error(e)
            continue
    prompt = f"""Ты финансовый аналитик. Составь утреннюю сводку для инвестора на русском языке.
    Данные портфеля:
    {portfolio_data}
    Сводка должна включать:
    1. Состояние портфеля — текущие цены и P&L по каждой позиции
    2. Технические сигналы — бычий/медвежий/нейтральный
    3. Важные новости
    4. Топ 3 рекомендации что делать сегодня   
    Пиши простым языком для обычного инвестора."""
    response = await llm.ainvoke([HumanMessage(content=prompt)])
    return response.content


async def run_morning_digest():
    logger.info("Starting morning digest generation")
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User))
        users = list(result.scalars().all())
        logger.info(f"Found {len(users)} users")
        for user in users:
            try:
                content = await generate_digest_for_user(user, session)
                if content is None:
                    continue
                digest = Digest(user_id=user.id, content=content)
                session.add(digest)
                await session.commit()
                logger.info(f"Digest saved for user: {user.id}")
            except Exception as e:
                logger.error(f"Failed to generate digest for user {user.id}: {e}")
                await session.rollback()


async def check_alerts():
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Alert).where(Alert.is_active == True)
        )
        alerts = list(result.scalars().all())
        for alert in alerts:
            try:
                price_data = get_stock_price(alert.ticker)
                current_price = price_data['close']
                triggered = (
                        alert.condition == "above" and current_price >= alert.threshold or
                        alert.condition == "below" and current_price <= alert.threshold
                )
                if triggered:
                    alert.is_active = False
                    content = f"Алерт сработал: {alert.ticker} цена {current_price} {alert.condition} {alert.threshold}"
                    digest = Digest(user_id=alert.user_id, content=content)
                    session.add(digest)
                    await session.commit()
                    logger.info(f"Alert triggered: {alert.ticker}")
            except Exception as e:
                logger.error(f"Failed to check alert {alert.id}: {e}")
                continue