import httpx
from datetime import datetime, timedelta
from app.config import settings

from functools import lru_cache
import zipfile
import io
import xml.etree.ElementTree as ET

from app.logger import logger


@lru_cache(maxsize=1)
def _load_corp_list() -> tuple:
    with httpx.Client() as client:
        response = client.get(
            'https://opendart.fss.or.kr/api/corpCode.xml',
            params={'crtfc_key': settings.DART_API_KEY}
        )
    zf = zipfile.ZipFile(io.BytesIO(response.content))
    xml_content = zf.read('CORPCODE.xml')
    root = ET.fromstring(xml_content)
    result = []
    for item in root.findall('list'):
        result.append({
            'corp_code': item.findtext('corp_code'),
            'corp_name': item.findtext('corp_name'),
            'stock_code': item.findtext('stock_code'),
        })
    return tuple(result)


def search_ticker_by_name(name: str) -> dict:
    """
    Search for a Korean stock ticker by company name.
    Use this when the user mentions a company by name instead of ticker code.
    Args:
        name: company name in Korean or English (e.g. '삼성전자', 'Samsung')
    """
    try:
        corps = _load_corp_list()
        for corp in corps:
            corp_name = corp.get('corp_name', '')
            stock_code = corp.get('stock_code', '')
            stock_code = stock_code.strip()
            if stock_code and stock_code.strip() and name.lower() in corp_name.lower():
                return {"ticker": stock_code, "name": corp_name}
        return {}
    except Exception as e:
        logger.error(f"Failed to search ticker by name '{name}': {e}")
        raise


def get_corp_code(ticker: str) -> str:
    """
    Get DART corporation code by stock ticker.
    DART uses its own corporation codes different from stock tickers.
    This code is required to fetch disclosures for a specific company.
    Args:
        ticker: Korean stock ticker (e.g. '005930' for Samsung Electronics)
    """
    # try:
    #     with httpx.Client() as client:
    #         params = {
    #             'crtfc_key': settings.DART_API_KEY,
    #             'stock_code': ticker
    #         }
    #
    #         response = client.get('https://opendart.fss.or.kr/api/company.json', params=params)
    #         data = response.json()
    #         if data.get('status') != '000':
    #             raise ValueError(f"DART API error: {data.get('message')}")
    #         logger.info(f"Corp code for {ticker}: {data['corp_code']}")
    #         return data['corp_code']
    # except Exception as e:
    #     logger.error(f"Failed to get corp code for {ticker}: {e}")
    #     raise
    corps = _load_corp_list()
    for corp in corps:
        if corp.get('stock_code', '').strip() == ticker:
            logger.info(f"Corp code for {ticker}: {corp['corp_code']}")
            return corp['corp_code']
    raise ValueError(f"Corp code not found for ticker: {ticker}")


def get_dart_disclosures(ticker: str = None, name: str = None, days: int = 30) -> list[dict]:
    """
    Get official corporate disclosures from DART (Korean financial disclosure system).
    Returns recent filings such as earnings reports, material facts, and regulatory announcements.
    Use this when the user asks about official company news, financial results, or regulatory filings.
    Args:
        ticker: Korean stock ticker (e.g. '005930' for Samsung Electronics)
        name: company name in Korean (e.g. '삼성전자') - used if ticker is not provided
        days: number of days to look back for disclosures (default 30)
    """
    logger.info(f"get_dart_disclosures called: ticker={ticker}, days={days}")
    if not ticker and not name:
        return [{"error": "Provide either ticker or company name"}]

    if not ticker and name:
        result = search_ticker_by_name(name)
        if not result:
            return [{"error": f"Company not found: {name}"}]
        ticker = result['ticker']
    start_date = (datetime.today() - timedelta(days=days)).strftime("%Y%m%d")
    end_date = datetime.today().strftime("%Y%m%d")
    corp_code = get_corp_code(ticker)
    try:
        with httpx.Client() as client:
            params = {
                'crtfc_key': settings.DART_API_KEY,
                'corp_code': corp_code,
                'bgn_de': start_date,
                'end_de': end_date,
                'page_count': 10,
            }
            response = client.get('https://opendart.fss.or.kr/api/list.json', params=params)
            data = response.json()
            if data.get('status') != '000':
                raise ValueError(f"DART API error: {data.get('message')}")
            logger.info(f"Got {len(data['list'])} disclosures for {ticker}")
            logger.info(f"get_dart_disclosures result: {len(data['list'])} disclosures")
            return data['list']
    except Exception as e:
        logger.error(f"Failed to get disclosures for {ticker}: {e}")
        raise


def get_financial_statements(ticker: str, year: str = None) -> list[dict]:
    """
    Get financial statements (income statement and balance sheet) for a Korean company from DART.
    Returns revenue, operating profit, net profit, assets, and equity.
    Use this when the user asks about financial results, revenue, profit, earnings, or company fundamentals.
    Args:
        ticker: Korean stock ticker (e.g. '005930' for Samsung Electronics)
        year: fiscal year (e.g. '2025'). Defaults to current year.
    """
    logger.info(f"get_financial_statements called: ticker={ticker}, year={year}")
    if not year:
        year = str(datetime.today().year -1)
    corp_code = get_corp_code(ticker)
    try:
        with httpx.Client() as client:
            params = {
                'crtfc_key': settings.DART_API_KEY,
                'corp_code': corp_code,
                'bsns_year': year,
                'reprt_code': '11013',
                'fs_div': 'CFS',
            }
            response = client.get('https://opendart.fss.or.kr/api/fnlttSinglAcnt.json', params=params)
            data = response.json()
            if data.get('status') != '000':
                raise ValueError(f"DART API error: {data.get('message')}")
            logger.info(f"get_financial_statements result: {len(data['list'])} items")
            return data['list']
    except Exception as e:
        logger.error(f"Failed to get financial statements for {ticker}: {e}")
        raise