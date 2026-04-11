from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph import StateGraph
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage
from langchain_mcp_adapters.client import MultiServerMCPClient

from tenacity import retry, stop_after_attempt, wait_fixed

from app.config import settings
from app.agent.state import AgentState
from app.constants import SYSTEM_PROMPT
from app.logger import logger


llm = ChatGroq(
    api_key=settings.GROQ_API_KEY,
    model=settings.LLM_MODEL,
    temperature=settings.LLM_TEMPERATURE,
    max_tokens=settings.LLM_MAX_TOKENS,
)


def build_graph(tools: list, checkpointer=None):
    llm_with_tools = llm.bind_tools(tools)
    tool_node = ToolNode(tools)

    async def _summarize_messages(messages: list) -> list:
        """Сжимает старые сообщения в summary если их больше порога."""
        if len(messages) <= settings.MAX_MESSAGES_BEFORE_SUMMARY:
            return messages

        # Делим на старые и свежие
        old_messages = messages[:-settings.SUMMARY_KEEP_LAST]
        recent_messages = messages[-settings.SUMMARY_KEEP_LAST:]

        logger.info(f"Summarizing {len(old_messages)} old messages")

        # Просим LLM сжать старые сообщения
        summary_prompt = f"""Summarize the following conversation concisely.
Keep key facts, data, and conclusions. Maximum 200 words.
Conversation:
{chr(10).join([f"{m.type}: {m.content[:500]}" for m in old_messages if m.content])}"""

        summary_response = await llm.ainvoke([SystemMessage(content=summary_prompt)])
        summary_text = f"[Previous conversation summary]: {summary_response.content}"

        logger.info(f"Summary created: {len(summary_text)} chars")

        # Возвращаем summary + свежие сообщения
        from langchain_core.messages import SystemMessage as SM
        return [SM(content=summary_text)] + recent_messages


    @retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
    async def invoke_with_retry(messages):
        response = await llm_with_tools.ainvoke(messages)
        return response

    async def agent_node(state: AgentState) -> dict:
        last_message = state['messages'][-1]
        logger.info(f"Agent received message: {last_message.content[:100]}")

        # Сжимаем если нужно
        messages = await _summarize_messages(state['messages'])
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + messages

        try:
            response = await invoke_with_retry(messages)
            logger.info(f"Agent response ready, tool_calls: {len(response.tool_calls)}")
            return {'messages': [response]}
        except Exception as e:
            logger.error(f"LLM error: {e}")
            raise

    graph = StateGraph(AgentState)

    graph.add_node('agent', agent_node)
    graph.add_node('tools', tool_node)

    graph.set_entry_point('agent')

    graph.add_conditional_edges('agent', tools_condition)
    graph.add_edge('tools', 'agent')

    return graph.compile(checkpointer=checkpointer)
