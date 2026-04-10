from tavily import TavilyClient
from app.config import settings
from app.logger import logger


tavily_client = TavilyClient(api_key=settings.TAVILY_API_KEY)  # ← другое имя


def tavily_search(query: str) -> str:
    """
    Search the web for news and information about Korean stocks, companies, and market events.
    Use this when the user asks about recent news, market sentiment, or external factors affecting a stock.
    Args:
        query: search query (e.g. 'Samsung Electronics news', '삼성전자 뉴스')
    """
    logger.info(f"Tavily search: {query}")
    try:
        results = tavily_client.search(
            query=query,
            max_results=settings.TAVILY_SEARCH_MAX_RESULTS
        )
        logger.info(f"Tavily search completed: {len(results.get('results', []))} results")
        return str(results)
    except Exception as e:
        logger.error(f"Tavily search error: {e}")
        raise