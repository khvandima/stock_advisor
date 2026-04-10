from fastapi import HTTPException, APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession
import uuid

from app.core.dependencies import get_current_user
from app.db.models import User, Alert
from app.db.session import get_db
from app.schemas.alert import AlertCreate, AlertResponse

from app.logger import logger

router = APIRouter(prefix="/alerts", tags=["alerts"])


@router.post('/')
async def create_alert(
        data: AlertCreate,
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
) -> AlertResponse:
    alert = Alert(
        user_id=user.id,
        ticker=data.ticker,
        threshold=data.threshold,
        condition=data.condition,
    )
    try:
        db.add(alert)
        await db.commit()
        await db.refresh(alert)
        logger.info(f"New alert added: {alert.ticker}")
    except Exception as e:
        logger.error(f"Failed to add new alert: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

    return AlertResponse.model_validate(alert)


@router.get('/')
async def get_alerts(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)) -> list[AlertResponse]:
    query = select(Alert).where(Alert.user_id == user.id)
    result = await db.execute(query)
    alerts = list(result.scalars().all())
    logger.info(f"Alerts fetched for user: {user.id}, count: {len(alerts)}")
    return alerts


@router.delete('/{alert_id}')
async def delete_alert(
        alert_id: uuid.UUID,
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
) -> dict:
    query = select(Alert).where(Alert.id == alert_id)
    result = await db.execute(query)
    alert = result.scalar_one_or_none()
    if alert is None:
        logger.error(f"Alert not found: {alert_id}")
        raise HTTPException(status_code=404, detail="Alert not found")
    if alert.user_id != current_user.id:
        logger.warning(f"Unauthorized delete attempt: user {current_user.id} tried to delete alert {alert_id}")
        raise HTTPException(status_code=403, detail="Not permitted")
    try:
        await db.delete(alert)
        await db.commit()
        logger.info(f"Alert is deleted: {alert_id} by user {current_user.id}")
    except Exception as e:
        await db.rollback()
        logger.error(f"Failed to delete alert {alert_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

    return {'message': 'deleted'}
