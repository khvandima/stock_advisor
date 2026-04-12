from mcp.server.fastmcp import FastMCP

from app.mcp.tools.krx_data import get_stock_price, get_stock_history
from app.mcp.tools.signals import get_signal
from app.mcp.tools.dart import get_dart_disclosures, get_financial_statements
from app.mcp.tools.tavily_news import tavily_search
from app.mcp.tools.portfolio import get_user_portfolio

import sys

from app.logger import logger

# import os
# os.environ["FASTMCP_PORT"] = "8001"
# os.environ["FASTMCP_HOST"] = "0.0.0.0"


mcp = FastMCP('stock-advisor-mcp')


mcp.add_tool(get_stock_price)
mcp.add_tool(get_stock_history)
mcp.add_tool(get_signal)
mcp.add_tool(get_dart_disclosures)
mcp.add_tool(get_financial_statements)
mcp.add_tool(tavily_search)
mcp.add_tool(get_user_portfolio)


if __name__ == "__main__":
    logger.remove()  # убираем все handlers
    logger.add("logs/mcp_server.log", level="INFO")
    # mcp.run(transport="sse")
    mcp.run(transport="stdio")
