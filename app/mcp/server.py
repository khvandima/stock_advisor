from fastmcp import FastMCP

from app.mcp.tools.krx_data import get_stock_price, get_stock_history
from app.mcp.tools.signals import get_signal

from app.logger import logger

import os
os.environ["FASTMCP_PORT"] = "8001"
os.environ["FASTMCP_HOST"] = "0.0.0.0"


mcp = FastMCP('stock-advisor-mcp')


mcp.add_tool(get_stock_price)
mcp.add_tool(get_stock_history)
mcp.add_tool(get_signal)


if __name__ == "__main__":
    logger.info("Starting MCP server on port 8001")
    mcp.run(transport="sse")
