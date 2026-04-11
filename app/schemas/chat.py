from pydantic import BaseModel

class ChatRequest(BaseModel):
    query: str
    thread_id: str | None = None


class ChatResponse(BaseModel):
    response: str
    thread_id: str
