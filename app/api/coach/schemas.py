from pydantic import BaseModel, Field


class CoachChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=500)


class CoachChatResponse(BaseModel):
    reply: str

class CoachMessageItem(BaseModel):
    role: str
    content: str
