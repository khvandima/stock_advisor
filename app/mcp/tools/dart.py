import httpx
from datetime import datetime, timedelta

from app.config import settings

from app.logger import logger


async def get_corp_code(ticker: str) -> str:
    """
    Get DART corporation code by stock ticker.
    DART uses its own corporation codes different from stock tickers.
    This code is required to fetch disclosures for a specific company.
    Args:
        ticker: Korean stock ticker (e.g. '005930' for Samsung Electronics)
    """
    try:
        async with httpx.AsyncClient() as client:
            params = {
                'crtfc_key': settings.DART_API_KEY,
                'stock_code': ticker
            }

            response = await client.get('https://opendart.fss.or.kr/api/company.json', params=params)
            data = response.json()
            if data.get('status') != '000':
                raise ValueError(f"DART API error: {data.get('message')}")
            logger.info(f"Corp code for {ticker}: {data['corp_code']}")
            return data['corp_code']
    except Exception as e:
        logger.error(f"Failed to get corp code for {ticker}: {e}")
        raise


async def get_dart_disclosures(ticker: str, days: int = 30) -> list[dict]:
    """
    Get official corporate disclosures from DART (Korean financial disclosure system).
    Returns recent filings such as earnings reports, material facts, and regulatory announcements.
    Use this when the user asks about official company news, financial results, or regulatory filings.
    Args:
        ticker: Korean stock ticker (e.g. '005930' for Samsung Electronics)
        days: number of days to look back for disclosures (default 30)
    """
    start_date = (datetime.today() - timedelta(days=days)).strftime("%Y%m%d")
    end_date = datetime.today().strftime("%Y%m%d")
    corp_code = await get_corp_code(ticker)
    try:
        async with httpx.AsyncClient() as client:
            params = {
                'crtfc_key': settings.DART_API_KEY,
                'corp_code': corp_code,
                'bgn_de': start_date,
                'end_de': end_date,
                'page_count': 10,
            }
            response = await client.get('https://opendart.fss.or.kr/api/list.json', params=params)
            data = response.json()
            if data.get('status') != '000':
                raise ValueError(f"DART API error: {data.get('message')}")
            logger.info(f"Got {len(data['list'])} disclosures for {ticker}")
            return data['list']
    except Exception as e:
        logger.error(f"Failed to get disclosures for {ticker}: {e}")
        raise

