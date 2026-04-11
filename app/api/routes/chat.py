from fastapi import APIRouter, HTTPException, Depends, Request
from langchain_core.messages import HumanMessage

from uuid import uuid4

from app.db.models import User
from app.schemas.chat import ChatRequest, ChatResponse
from app.core.dependencies import get_current_user

from app.logger import logger

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post('/')
async def chat(req: Request, data: ChatRequest, current_user: User = Depends(get_current_user)) -> ChatResponse:
    user_id = str(current_user.id)
    logger.info(f"Chat request from user: {current_user.id}, thread: {data.thread_id}")
    thread_id = data.thread_id or f"{user_id}_{uuid4()}"

    graph = req.app.state.graph

    try:
        config = {'configurable': {'thread_id': thread_id}}

        result = await graph.ainvoke({
            'messages': [HumanMessage(content=data.query)],
            'user_id': str(current_user.id),
        }, config=config)

        last_message = result['messages'][-1]
        logger.info(f'Chat response ready for user: {current_user.email}')

        return ChatResponse(
            response=last_message.content,
            thread_id=thread_id,
        )
    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail='Agent unavailable')

