from langgraph.graph import MessagesState
from typing import Optional

class AgentState(MessagesState):
    user_id: str
    summary: Optional[str] = None
